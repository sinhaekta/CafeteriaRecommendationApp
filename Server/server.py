import socket
import signal
import json
import config
from ServerController.route import Route  

def signal_handler(sig, frame):
    print("\nStopping server...")
    server_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def start_server():
    SERVER_HOST = config.SERVER_HOST 
    SERVER_PORT = config.SERVER_PORT

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((SERVER_HOST, SERVER_PORT))

        server_socket.listen(5) 

        print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")

            data = client_socket.recv(2048).decode('utf-8')
            print(f"Received data from client: {data}")

            try:
                json_data = json.loads(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                continue 
            print(json_data)
            try:
                response = Route.redirect_client_data(json_data)
                print(response, type(response))
                response_json = json.dumps(response) 
            except Exception as e:
                print(f"Error processing request: {e}")
                response_json = "error"
                continue  

            client_socket.send(response_json.encode('utf-8'))
            print("Done")

            client_socket.close()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server_socket.close()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
    start_server()