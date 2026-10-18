#!/bin/sh
# Storage appliance (Debian 13 VM, data disk /dev/vdc, switch NIC 10.99.0.2/24 with MTU 9000).
# Exports one LV over iSCSI (LIO) and one over NVMe/TCP (nvmet). Spike only: no authentication.
set -eu
CLIENT_IQN=${1:?client initiator name, from /etc/iscsi/initiatorname.iscsi}
apt-get install -y targetcli-fb lvm2
modprobe nvmet nvmet-tcp
pvcreate /dev/vdc && vgcreate vols /dev/vdc
lvcreate -L 20G -n iscsi vols && lvcreate -L 18G -n nvme vols

# iSCSI: the backstore name becomes the SCSI model, the serial must be set before export
T=iqn.2026-09.io.ownpaas:srv-1
targetcli /backstores/block create HC_Volume_301 /dev/vols/iscsi
echo HC_Volume_301 > /sys/kernel/config/target/core/iblock_0/HC_Volume_301/wwn/vpd_unit_serial
targetcli /backstores/block/HC_Volume_301 set attribute emulate_model_alias=1
targetcli /iscsi create $T
targetcli /iscsi/$T/tpg1 set attribute authentication=0
targetcli /iscsi/$T/tpg1/luns create /backstores/block/HC_Volume_301 add_mapped_luns=false
targetcli /iscsi/$T/tpg1/acls create "$CLIENT_IQN"

# NVMe/TCP: plain configfs, model and serial are free-form
N=/sys/kernel/config/nvmet
S=$N/subsystems/hc-volume-302
mkdir -p $S/namespaces/1
echo 1 > $S/attr_allow_any_host
echo HC_Volume_302 > $S/attr_serial
echo HC_Volume_302 > $S/attr_model
echo /dev/vols/nvme > $S/namespaces/1/device_path
echo 1 > $S/namespaces/1/enable
mkdir -p $N/ports/1
echo 10.99.0.2 > $N/ports/1/addr_traddr
echo tcp > $N/ports/1/addr_trtype
echo 4420 > $N/ports/1/addr_trsvcid
echo ipv4 > $N/ports/1/addr_adrfam
ln -s $S $N/ports/1/subsystems/

# client side:
#   iscsiadm -m discovery -t st -p 10.99.0.2 && iscsiadm -m node -T $T -p 10.99.0.2:3260 --login
#   nvme connect -t tcp -a 10.99.0.2 -s 4420 -n hc-volume-302
#   (without nvme-cli: echo "transport=tcp,traddr=10.99.0.2,trsvcid=4420,nqn=hc-volume-302" > /dev/nvme-fabrics)
