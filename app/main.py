import socket
import threading
from sys import argv
import gzip
import io

def parse_request(request_string):
    lines = request_string.split('\r\n')
    method, path, http_version = lines[0].split()

    headers = {}
    for line in lines[1:]:
        if not line:
            break
        key, value = line.split(': ', 1)
        headers[key] = value

    body = None
    if '\r\n\r\n' in request_string:
        body = request_string.split('\r\n\r\n', 1)[1]

    return method, path, http_version, headers, body

def validateEncoding(encodings):
    invalid_encodings = ['encoding-1', 'encoding-2', 'invalid_encoding']
    validateEncodings = filter(lambda encoding: encoding.strip() not in invalid_encodings, encodings)
    return list(validateEncodings)

def getResponseTxt(method, path, http_version, headers, body):
    if path == "/":
        return "HTTP/1.1 200 OK\r\n\r\n".encode()
    elif "/echo" in path:
        content = path.split('/')[-1]
        content_length = len(path.split('/')[-1])
        if "Accept-Encoding" in headers and headers['Accept-Encoding'] != 'invalid-encoding':
            validEncoding = validateEncoding(headers['Accept-Encoding'].split(','))
            if len(validEncoding) != 0:
                if validEncoding[0] == "gzip":
                    content_bytes = content.encode("utf-8")
                    compressed_content = io.BytesIO()
                    with gzip.GzipFile(fileobj=compressed_content, mode='wb') as f:
                        f.write(content_bytes)
                    compressed_data = compressed_content.getvalue()
                    return b"HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: " + str(len(compressed_data)).encode() + b"\r\n\r\n" + compressed_data
                return f"HTTP/1.1 200 OK\r\nContent-Encoding: {validEncoding[0]}\r\nContent-Type: text/plain\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
        return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{content}".encode()
    elif "/user-agent" in path:
        content_body = headers['User-Agent']
        content_length = len(content_body)
        return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{content_body}".encode()
    elif "/files" in path:
        f_name = path.split("/")[-1]
        try:
            if method == "GET":
                with open(argv[2] + f_name) as f:
                    content = f.read()
                    cont_length = len(content)
                    return f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length:{cont_length}\r\n\r\n{content}".encode()
            elif method == "POST":
                filepath = f"{argv[2]}/{f_name}"
                with open(filepath, "wb") as file:
                    file.write(body.encode("utf-8"))
                    return f"HTTP/1.1 201 Created\r\n\r\n".encode()
        except FileNotFoundError:
            return "HTTP/1.1 404 Not Found\r\n\r\n".encode()
    else:
        return 'HTTP/1.1 404 Not Found\r\n\r\n'.encode()

def parseRequest(client):
    lines = client.recv(4096).decode().split(' ')
    method = lines[0]
    path = lines[1]
    return method, path, lines

def sendResponse(client, text):
    client.sendall(text)

def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221))
    server_socket.listen()

    while True:
        client, addr = server_socket.accept()
        lines = client.recv(4096).decode()
        method, path, http_version, headers, body = parse_request(lines)
        response = getResponseTxt(method, path, http_version, headers, body)
        threading.Thread(target=sendResponse, args=(client, response)).start()

if __name__ == "__main__":
    main()
