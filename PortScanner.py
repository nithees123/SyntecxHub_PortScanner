import socket
import sys
import subprocess
from datetime import datetime

subprocess.call("clear",shell=True)

rs=input("Enter a Host IP to scan:")
x=int(input("Enter the starting port:"))
y=int(input("Enter the ending port:"))
rsIP=socket.gethostbyname(rs)
print("~"*60)
print("Scanning Host:",rsIP)
print("~"*60)
t1=datetime.now()

try:
    for port in range(x,y+1):
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result=sock.connect_ex((rsIP,port))
        if result==0:
            print(f"Port {port} :open")
        else:
            print(f"Port {port} :close")
            
        sock.close()
except KeyboardInterrupt:
    print("You pressed CTRL+C")
    sys.exit()
except Exception:
    print("Host couldn't resolved !! /nExiting...........")
    sys.exit()

t2=datetime.now()
final=t2-t1
print(f"time taken {final} sec")
