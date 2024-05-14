# Uncomment this to pass the first stage
# import socket
import socket

def main():


    def getResponse(method, path, response_body):
      
        if path == "/":
            return "HTTP/1.1 200 OK\r\n\r\n"
        elif "/echo" in path:
            content = path.split('/')[-1]
            content_length = len(path.split('/')[-1])

            return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{content}"
        
        elif "/user-agent" in path:
            
            content_length = len(response_body)

            return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{response_body}"


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

    print(lines[-1].strip())

    
    method = lines[0]
    path = lines[1]
    response_body = lines[-1].strip()

    print("method and path", method, path)

    response = getResponse(method, path, response_body)
    client.sendall(response.encode())


    # client.close()

    
if __name__ == "__main__":
    main()