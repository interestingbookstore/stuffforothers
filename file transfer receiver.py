import socket

# ----------------------------------------
host = ???  # This should be a string
port = ???  # This should be an integer
name_id = ???  # When you ask to receive a file from a sender, they're
               # given your IP address, as well as this string. Write in
               # your name, or something...
# ----------------------------------------

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    print(f'Requesting to connect to {host} on port {port}')
    s.sendall(name_id.encode())
    while True:
        code = s.recv(1024)
        if code != b'':
            print('Host accepted request')
            code = code.decode()
            name, code = code.split('\n', 1)
            extension = '.' + name.split('.')[-1]
            name = name[:-len(extension)]

            add = False
            while True:
                try:
                    with open(name + extension, 'x+') as f:
                        f.write(code)
                        break
                except FileExistsError:
                    if not add:
                        name += '(1)'
                        add = True
                    else:
                        idk = name.rindex('(') + 1
                        name = name[:idk] + str(int(name[idk]) + 1) + ')'
            print(f'File created successfully as "{name + extension}" in current working directory')
            s.sendall(b'1')
            break
