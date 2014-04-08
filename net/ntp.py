#coding:utf8
import time
import socket
import struct
host="time.nist.gov"
port=37
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.sendto("",(host,port))

buf=s.recvfrom(2048)[0]
if len(buf)!=4:
    sys.exit(1)
secs=struct.unpack("!I",buf)[0]-2208988800 # 获取到的是1900年到现在的二进制秒数，我们需要的是1970年到现在的秒数
print time.ctime(int(secs))
