import os
src_port = 57372
dst_port = 8000
bsrc = src_port.to_bytes(2, 'big')

bdst = dst_port.to_bytes(2, 'big')

seq_num = os.urandom(4)
ack_num = seq_num[:3] + (int(seq_num[3]) + 1).to_bytes(1, 'big')
flags = int(b'001', 2).to_bytes(1, 'big')

print(flags)
header = bsrc + bdst+seq_num+ack_num+flags
