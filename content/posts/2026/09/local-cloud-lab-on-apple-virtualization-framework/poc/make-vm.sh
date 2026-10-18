#!/bin/sh
# make-vm.sh <dir> <name> <nat-mac> <ssh-public-key-file>: root disk clone and NoCloud seed for vzprobe.
# The seed is a FAT disk labeled CIDATA: an ISO 9660 seed on a virtio disk was ignored by cloud-init.
set -eu
dir=$1 name=$2 mac=$3 key=$4
mkdir -p "$dir/seed"
/bin/cp -c debian-13-generic-arm64.raw "$dir/root.raw"   # APFS clone, instant
truncate -s 20G "$dir/root.raw"
cat > "$dir/seed/meta-data" <<EOT
instance-id: $name
local-hostname: $name
public-keys:
  - $(cat "$key")
EOT
printf '#cloud-config\ndisable_root: false\n' > "$dir/seed/user-data"
cat > "$dir/seed/network-config" <<EOT
version: 2
ethernets:
  eth0:
    match: {macaddress: "$mac"}
    set-name: eth0
    dhcp4: true
    dhcp-identifier: mac   # otherwise the macOS DHCP server keys the lease by DUID
EOT
hdiutil create -quiet -fs "MS-DOS FAT12" -volname CIDATA -srcfolder "$dir/seed" -format UDRW -size 4m "$dir/seed.dmg"
dev=$(hdiutil attach -nomount "$dir/seed.dmg" | head -1 | awk '{print $1}')
/bin/dd if="$(echo "$dev" | sed s/disk/rdisk/)" of="$dir/seed.iso" bs=1m 2>/dev/null
hdiutil detach "$dev" >/dev/null
