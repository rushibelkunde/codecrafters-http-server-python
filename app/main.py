# Uncomment this to pass the first stage
# import socket
import socket

def main():


    def getResponse(method, path):
      
        if path == "/":
            return "HTTP/1.1 200 OK\r\n\r\n"
        elif "/echo" in path:
            content = path.split('/')[-1]
            content_size = len(path.split('/')[-1])

            return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_size}\r\n\r\n{content}"


        else:
            return 'HTTP/1.1 404 Not Found\r\n\r\n'

    GET = "GET"
    POST = "POST"
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    # Uncomment this to pass the first stage
    #
    # server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket.accept() # wait for client
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket.accept() 
    client, addr = server_socket.accept()


    lines = client.recv(4096).decode().split(' ')

    print(lines)

    
    method = lines[0]
    path = lines[1]
    print("method and path", method, path)

    response = getResponse(method, path)
    client.sendall(response.encode())


    # client.close()

    
if __name__ == "__main__":
    main()