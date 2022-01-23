import socket
from pathlib import Path

# ----------------------------------------
host = ''  # This should be a string
port = 0000  # This should be an integer
name_id = ''  # When you ask to receive a file from a sender, they're
#               given your IP address, as well as this string. Write in
#               your name, or something...
# ----------------------------------------

# -----------------------------------------------------------------------------------------------

def send(text):
    global s

    text = str(text)
    s.sendall(f'{len(text)},{text}'.encode())


# -----------------------------------------------------------------------------------------------

def receive():
    total_characters, response = s.recv(1024).decode().split(',', 1)
    total_characters = int(total_characters)
    characters_received = len(response)

    while characters_received < total_characters:
        response += s.recv(1024).decode()
        characters_received = len(response)

    return response


# -----------------------------------------------------------------------------------------------

print(f'Connecting to {host} on port {port}', end='')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    print(f'\rConnected to {host} on port {port}')
    send(name_id)

    # Wait for host to accept, then accept
    response = receive()
    if response == '1':
        if input('Host wants to share code, accept? (y/n): ') == 'y':
            send(1)

            # -----  Receive the code  --------------------
            code = receive()
            print('Code Received')
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
                        name += ' (1)'
                        add = True
                    else:
                        idk = name.rindex(' (') + 2
                        name = name[:idk] + str(int(name[idk]) + 1) + ')'
            print(f'File created successfully as "{name + extension}" at {Path.cwd()}/{name + extension}')
            send(1)
        else:
            send(0)
    elif response == '0':
        print('Host denied request')
