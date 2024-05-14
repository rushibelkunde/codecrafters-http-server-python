# Uncomment this to pass the first stage
# import socket
import socket
import threading
from sys import argv


def getResponseTxt(method, path, response_body, lines):
        if path == "/":
            return "HTTP/1.1 200 OK\r\n\r\n"
        elif "/echo" in path:
            content = path.split('/')[-1]
            content_length = len(path.split('/')[-1])
            return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{content}"
        elif "/user-agent" in path:
            content_length = len(lines[2].split(" ")[1].strip())
            print("cccc",content_length)
            return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length} \r\n\r\n {response_body}"
        elif "/files" in path:
            f_name = path.split("/")[-1]
            try:
                if method == "GET":
                    with open(argv[2] + f_name) as f:
                        content = f.read()
                        cont_length = len(content)
                       
                        return f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: "+ str(cont_length)+ "\r\n\r\n"+ content
                elif method == "POST":
            
                    filepath = f"{argv[2]}/{f_name}"
                    with open(filepath, "wb") as file:
                        file.write(response_body.encode("utf-8"))
                        return f"HTTP/1.1 201 Created\r\n\r\n"
                     
            except FileNotFoundError:
                    return "HTTP/1.1 404 Not Found\r\n\r\n"    
        else:
            return 'HTTP/1.1 404 Not Found\r\n\r\n'
        
def parseRequest(client):
    lines = client.recv(4096).decode().split('\r\n')

    print("lines",lines)
    method = lines[0].split(' ')[0]
    path =  lines[0].split(' ')[1]
    response_body = lines[-1]
    return method, path, response_body , lines

def sendResponse(client,text):
     client.sendall(text.encode("UTF-8"))
     

def main():

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    # Uncomment this to pass the first stage
    #
    # server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket.accept() # wait for client
    server_socket = socket.create_server(("localhost", 4221))
    server_socket.listen()
    # server_socket.accept() 

    while True:
        client, addr = server_socket.accept()
        method, path, response_body, lines = parseRequest(client)
        print("remote", method, path, response_body)
        response = getResponseTxt(method, path, response_body, lines)
        # print('response',response)
        threading.Thread(target=sendResponse, args=(client,response )).start()




    # client.close()

    
if __name__ == "__main__":
    main()