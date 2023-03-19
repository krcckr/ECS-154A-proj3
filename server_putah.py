import sys
import socket
ip = sys.argv[2]
wel_port = int(sys.argv[4])
conn_port = 8000 if wel_port != 8000 else 7000
databuf = []

#custom tcp header format
'''+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |          Source Port          |       Destination Port        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                        Sequence Number                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Acknowledgment Number                      |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |A|S|F| 
   |C|Y|I| 
   |K|N|N| 
   +-+-+-+'''

def buildSYNACK(data):
    #Source Port
    src_port = wel_port.to_bytes(2, 'big')

    #Destination Port
    dst_port = data[:2]

    #Sequence Number
    seq_num = data[2:6]

    #Acknowledgment number is sequence number incremented by 1
    ack_num = seq_num[:3] + (int(seq_num[3]) + 1).to_bytes(1, 'big')

    #Flags composed of ACK SYN FIN
    flags = int(b'110', 2).to_bytes(1, 'big')

    return src_port+dst_port+seq_num+ack_num+flags

def buildFIN(data):
    #Source Port
    src_port = conn_port.to_bytes(2, 'big')

    #Destination Port
    dst_port = data[:2]

    #Sequence Number
    seq_num = data[2:6]

    #Acknowledgment number is sequence number incremented by 1
    ack_num = seq_num[:3] + (int(seq_num[3]) + 1).to_bytes(1, 'big')

    #Flags composed of ACK SYN FIN
    flags = int(b'001', 2).to_bytes(1, 'big')

    return src_port+dst_port+seq_num+ack_num+flags

def get_msg_type(data):
    if data[-1:] == b'\x04':
        return 'ACK'
    elif data[-1:] == b'\x02':
        return 'SYN'
    elif data[-1:] == b'\x01':
        return 'FIN'
    return 'DATA'


def accept(sokect):   
    data, addr = s.recvfrom(1024)
    databuf.append(data)
    if get_msg_type(data) == 'SYN':
        SYNACK = buildSYNACK(data)
        s.sendto(SYNACK, addr)
    elif get_msg_type(data) == 'ACK':
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        conn.bind((ip, conn_port))
        conn.listen()
    return [conn, addr[1]]
    

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((ip, wel_port))
    conn, src_port = accept(s)
    try:
        with conn:
            print(ip, src_port)
            while True:
                data, addr = conn.recvfrom(1024)
                if data.decode() == "ping":
                    conn.sendto(b"pong", (ip, src_port))
                
    except KeyboardInterrupt:
        FIN = buildFIN()
        conn.sendto(FIN, (ip, src_port))
        while True:
            data, addr = conn.recvfrom(1024)
            if get_msg_type(data) == 'ACK':
                conn.close()
            
