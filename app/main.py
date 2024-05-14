# Uncomment this to pass the first stage
# import socket
import socket
import threading



def getResponseTxt(method, path, response_body):
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
        
def parseRequest(client):
    lines = client.recv(4096).decode().split(' ')
    # print(lines[-1].strip())
    method = lines[0]
    path = lines[1]
    response_body = lines[-1].strip()
    return method, path, response_body

def sendResponse(client,text):
     client.sendall(text.encode("UTF-8"))
     

def main():

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    # Uncomment this to pass the first stage
    #
    # server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket.accept() # wait for client
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen()
    # server_socket.accept() 

    while True:
        client, addr = server_socket.accept()
        method, path, response_body = parseRequest(client)
        print("remote", method, path, response_body)
        response = getResponseTxt(method, path, response_body)
        # print('response',response)
        threading.Thread(target=sendResponse, args=(client,response ))




    # client.close()

    
if __name__ == "__main__":
    main()