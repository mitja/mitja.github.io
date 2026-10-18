#!/bin/sh
# bench.sh <name> <device>: raw-device fio jobs, then an etcd-style fdatasync test on ext4
set -eu
name=$1 dev=$2 out=/root/bench/$1; mkdir -p $out
run() { fio --name=$1 --filename=$dev --direct=1 --ioengine=libaio --time_based --runtime=${RT:-20} --group_reporting --output-format=json --output=$out/$1.json "$@" >/dev/null 2>&1 || true; }
job() { n=$1; shift; fio --name=$n --filename=$dev --direct=1 --ioengine=libaio --time_based --runtime=20 --group_reporting --output-format=json --output=$out/$n.json "$@" >/dev/null; }
job randread  --rw=randread  --bs=4k --iodepth=32 --numjobs=1
job randwrite --rw=randwrite --bs=4k --iodepth=32 --numjobs=1
job randrw    --rw=randrw --rwmixread=70 --bs=4k --iodepth=16 --numjobs=2
job lat-qd1   --rw=randwrite --bs=4k --iodepth=1 --numjobs=1
job seqwrite  --rw=write --bs=1M --iodepth=4 --numjobs=1
job seqread   --rw=read  --bs=1M --iodepth=4 --numjobs=1
mkfs.ext4 -q -F $dev; mkdir -p /mnt/bench; mount $dev /mnt/bench
fio --name=etcd --directory=/mnt/bench --rw=write --ioengine=sync --fdatasync=1 --size=22m --bs=2300 --output-format=json --output=$out/etcd.json >/dev/null
umount /mnt/bench
echo done $name
