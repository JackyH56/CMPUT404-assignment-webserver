#  coding: utf-8 
import socketserver
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

#cd uofastuff/winter2021/cmput404/assignments/cmput404-assignment-webserver

class MyWebServer(socketserver.BaseRequestHandler):
    def handle(self):
        """
        Handles receiving request, opening file and sending back the files that are requested
        """
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        file = self.get_file(self.data)
        if isinstance(file, str):
            try:
                f = open("www" + file[:-1], "r")
                content_type = self.get_content_type(file)
                print("file opened = www" + file[:-1])
                print("content type = " + content_type)
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n", "utf-8"))
                self.request.sendall(bytearray("Content-Type: " + content_type + "\r\n\n", "utf-8"))
                self.request.sendall(bytearray(f.read(), "utf-8"))
                f.close()
            except:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\nError 404 Could not find the page you were looking for", "utf-8"))

    def get_file(self, data):
        """
        Handles parsing the GET request and returning the proper file name

        Parameters
            data (bytes): The request that needs to be parsed
    
        Returns
            file: the proper file name
        """
        data = data.decode()
        if data == "":
            return None
        file, host = data.split("HTTP/1.1")
        #remove whitespace
        file = file.strip()
        method, file = file.split(" ")
        method = method.strip()
        if method != "GET":
            return self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n", "utf-8"))
        else:
            if file[-1] != "/":
                return self.request.sendall(bytearray("HTTP/1.1 301 Moved Permenantly\r\nLocation: http://127.0.0.1:8080" + file + "/\r\n\n", "utf-8"))
            
            if file == "/" or (not file.endswith("css/") and not file.endswith("html/")):
                return file + "index.html/"
            elif file.endswith("css/") and file != "/base.css/":
                return file.replace("index.html/", "")
            else:
                return file

    def get_content_type(self, file):
        """
        Handles figuring out the right mime-type for the file

        Parameters
            file (str): The file we need to get the mime-type for
    
        Returns
            the mime-type as a string
        """
        if file.endswith(".html/"):
            return "text/html"

        elif file.endswith(".css/"):
            return "text/css"

        else:
            print("How'd you get here? Error can't get content type for :" + file)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
