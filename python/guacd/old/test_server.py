import socket


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        received = b''
        while True:
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                break
            print("from connected user: " + str(data))
            breakpoint()
            data = input(' -> ')
            conn.send(data.encode())  # send data to the client
            # data = conn.recv(1024)
            # if not data:
            #     break
            # elif data.endswith(b'\n'):
            #     if received == b'quit':
            #         break
            #     else:
            #         conn.sendall(received + b'\n')
            #         received = b''
            # else:
            #     received += data
