import json,sys
base=sys.argv[1]
names=['virtio','usb','iscsi','nvmetcp']
def load(n,j): return json.load(open(f'{base}/{n}/{j}.json'))['jobs'][0]
print("| metric | "+" | ".join(names)+" |"); print("|---"*(len(names)+1)+"|")
def row(label,f):
    vals=[]
    for n in names:
        try: vals.append(f(n))
        except Exception as e: vals.append('err')
    print(f"| {label} | "+" | ".join(vals)+" |")
row("4k randread qd32 IOPS", lambda n: f"{load(n,'randread')['read']['iops']:,.0f}")
row("4k randwrite qd32 IOPS", lambda n: f"{load(n,'randwrite')['write']['iops']:,.0f}")
row("4k randrw 70/30 qd16x2 IOPS", lambda n: f"{load(n,'randrw')['read']['iops']+load(n,'randrw')['write']['iops']:,.0f}")
row("4k randwrite qd1 IOPS", lambda n: f"{load(n,'lat-qd1')['write']['iops']:,.0f}")
row("4k randwrite qd1 p99 (ms)", lambda n: f"{load(n,'lat-qd1')['write']['clat_ns']['percentile']['99.000000']/1e6:.2f}")
row("1M seq write MB/s", lambda n: f"{load(n,'seqwrite')['write']['bw_bytes']/1e6:,.0f}")
row("1M seq read MB/s", lambda n: f"{load(n,'seqread')['read']['bw_bytes']/1e6:,.0f}")
def etcd(n,p): return f"{load(n,'etcd')['sync']['lat_ns']['percentile'][p]/1e6:.2f}"
row("etcd fdatasync p50 (ms)", lambda n: etcd(n,'50.000000'))
row("etcd fdatasync p99 (ms)", lambda n: etcd(n,'99.000000'))
row("etcd write IOPS", lambda n: f"{load(n,'etcd')['write']['iops']:,.0f}")
