| metric | virtio | usb | iscsi | nvmetcp |
|---|---|---|---|---|
| 4k randread qd32 IOPS | 136,889 | 6,308 | 39,240 | 41,938 |
| 4k randwrite qd32 IOPS | 14,238 | 4,897 | 12,100 | 14,045 |
| 4k randrw 70/30 qd16x2 IOPS | 32,243 | 4,978 | 27,272 | 30,039 |
| 4k randwrite qd1 IOPS | 11,713 | 4,923 | 3,059 | 3,942 |
| 4k randwrite qd1 p99 (ms) | 0.15 | 0.36 | 0.56 | 0.45 |
| 1M seq write MB/s | 1,126 | 1,448 | 248 | 233 |
| 1M seq read MB/s | 1,135 | 936 | 582 | 567 |
| etcd fdatasync p50 (ms) | 9.63 | 0.52 | 6.13 | 10.55 |
| etcd fdatasync p99 (ms) | 13.04 | 1.02 | 8.59 | 13.04 |
| etcd write IOPS | 121 | 2,050 | 158 | 113 |
