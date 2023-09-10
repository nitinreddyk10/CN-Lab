import socket
s=socket.socket()
host=socket.gethostname()
print(host)
port=12345
s.bind(('',port))
s.listen(5)
print("Socket is listening")
while True:
    c, addr=s.accept()
    print("connection received from",addr)
    c.send("Thank you :)" .encode())
    c.close()
    break
