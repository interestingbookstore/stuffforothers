import pyperclip
import socket

host = ''
port = 

code = input('Name: ')
if code[-3:] != '.py' or code[-4:] != '.txt':
    code += '.py'
code += '\n' + pyperclip.paste()

print('-----------------')
print(code)
print('------------------')


def send(text):
    text = str(text)
    connection.sendall(f'{len(text)},{text}'.encode())


# -----------------------------------------------------------------------------------------------

def receive():
    total_characters, response = connection.recv(1024).decode().split(',', 1)
    total_characters = int(total_characters)
    characters_received = len(response)

    while characters_received < total_characters:
        response += connection.recv(1024).decode()
        characters_received = len(response)

    return response


try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        print('Looking...', end='')
        s.listen()
        connection, address = s.accept()
        name_id = receive()
        print(f'\rConnection established with {name_id} ({address[0]})')
        with connection:
            if input(f'Send to {name_id}? (y/n): ').lower() == 'y':
                send(1)
                print('Waiting for receiver response...')
                response = receive()
                if response == '1':
                    send(code)
                    print('Code sent!')
                    response = receive()
                    if response == '1':
                        print('Code received!')
                elif response == '0':
                    print('Received declined...')
except KeyboardInterrupt:
    s.close()
