# Uncomment this to pass the first stage
# import socket
import socket
import threading
from sys import argv

def parse_request(request_string):
    # Split the request string into lines
    lines = request_string.split('\r\n')
    
    # Extract method, path, and HTTP version from the first line
    method, path, http_version = lines[0].split()

    # Extract headers
    headers = {}
    for line in lines[1:]:
        if not line:
            break
        key, value = line.split(': ', 1)
        headers[key] = value

    # Extract response body
    body = None
    if '\r\n\r\n' in request_string:
        body = request_string.split('\r\n\r\n', 1)[1]

    return method, path, http_version, headers, body

def validateEncoding(encodings):
    print(encodings)
    invalid_encodings = ['encoding-1', 'encoding-2', 'invalid_encoding']
    validateEncodings = filter(lambda encoding: encoding.strip() not in invalid_encodings, encodings)
    return list(validateEncodings)




def getResponseTxt(method, path, http_version, headers, body):
        if path == "/":
            return "HTTP/1.1 200 OK\r\n\r\n"
        elif "/echo" in path:
            content = path.split('/')[-1]
            content_length = len(path.split('/')[-1])
            if("Accept-Encoding" in headers and headers['Accept-Encoding'] != 'invalid-encoding'):
                validEncoding = validateEncoding(headers['Accept-Encoding'].split(','))
                print(validEncoding)
                if len(validEncoding) != 0:
                    if validEncoding[0] == "gzip":
                        return  f"HTTP/1.1 200 OK\r\nContent-Encoding: {validEncoding[0]}\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{content}"
                    
                    return  f"HTTP/1.1 200 OK\r\nContent-Encoding: {validEncoding[0]}\r\nContent-Type: text/plain\r\nContent-Length: {len(body)}\r\n\r\n{body}"

            return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{content}"
        elif "/user-agent" in path:
            content_body = headers['User-Agent']
            content_length = len(content_body)
            return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{content_body}"
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
                        file.write(body.encode("utf-8"))
                        return f"HTTP/1.1 201 Created\r\n\r\n"
                     
            except FileNotFoundError:
                    return "HTTP/1.1 404 Not Found\r\n\r\n"    
        else:
            return 'HTTP/1.1 404 Not Found\r\n\r\n'
        
def parseRequest(client):
    lines = client.recv(4096).decode().split(' ')

    print(lines)
    method = lines[0]
    path = lines[1]
    return method, path, lines

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
        lines = client.recv(4096).decode()
        method, path , http_version, headers,  body = parse_request(lines)
        print("remote", method, path)
        response = getResponseTxt(method, path, http_version, headers, body)
        # print('response',response)
        threading.Thread(target=sendResponse, args=(client,response )).start()




    # client.close()

    
if __name__ == "__main__":
    main()