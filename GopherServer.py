'''
Gopher protocol implementation - Server
Authors: Emilee F, Malcolm M, Steph H
Credit to : Amy Csizmar Dalal for Sockets Lab starter file
CS 331, Spring 2018
Date:  12 April 2018
'''
import sys, socket

class TCPServer:
    def __init__(self, port=50000):
        self.port = port
        self.host = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    # Returns list containing each line in .links file
    def getDirectory(self, path):
        file = open(path + ".links", "r")
        text = file.read()
        lines = text.split("\n")
        return lines
    
    # Checks if folder contains inputted item
    def doesFolderContain(self, lines, item):
        for line in lines:
            if line.split("\t")[1] == item:
                return True
        return False
    
    # Returns the item's type if text file (0) or directory (1)
    def getItemType(self, lines, item):
        for line in lines:
            if line.split("\t")[1] == item:
                if line.split("\t")[0][0] == '0':
                    return 0
                elif line.split("\t")[0][0] == '1':
                    return 1
                else:
                    return None
    
    # Returns file if text file or returns .links if directory
    def openPathPart(self, currentPath, pathPart):
        lines = self.getDirectory(currentPath)
        if self.getItemType(lines, pathPart) == 0:
            file = open(currentPath + pathPart + ".txt", "r")
        elif self.getItemType(lines, pathPart) == 1:
            file = open(currentPath + pathPart + "/.links", "r")
            
        return file
    
    # Returns list of the path parts of inputted query
    def splitQuery(self, query):
        # Removes .txt extension if it exists
        if len(query)>4 and query[-4:] == ".txt":
            query = query[0:-4]
        queryPathParts = query.split("/")
        if queryPathParts[len(queryPathParts)-1] == "":
            queryPathParts.remove("")
            queryPathParts[len(queryPathParts)-1] += "/"
        return queryPathParts
    
    # Returns the destination file specified by the client
    def openDestinationFileOrDirectory(self, queryPathParts, clientSock):
        currentPath = "Content/"
        
        for i in range(len(queryPathParts)): 
            pathPart = queryPathParts[i]
            if i != len(queryPathParts)-1:
                pathPart += "/"

            lines = self.getDirectory(currentPath)
            if self.doesFolderContain(lines, pathPart):
                if self.getItemType(lines, pathPart) == None:
                    clientSock.sendall(("Unknown file type. \n.").encode("ascii"))
                    return
                elif self.getItemType(lines, pathPart) == 0 and i != len(queryPathParts)-1:
                    clientSock.sendall(("Invalid file path. \n.").encode("ascii"))
                    return
                elif i == len(queryPathParts)-1:
                    file = self.openPathPart(currentPath, pathPart)
            else:
                clientSock.sendall("File or Directory Not Found. \n.".encode("ascii"))
                return

            currentPath += pathPart
        return file
    
    # Formats inputted file to specifications and returns its text
    def formatResponseFile(self, file):
        text = file.read()
        text += "\n."
        
        # Limits line length to 70 characters
        lines = text.split("\n")
        newLines = lines
        for i in range(len(lines)):
            lines[i] = lines[i][0:70]
            newLines[i] = lines[i]
            
        text = "\n".join(newLines)
        
        return text
    
    # Receives request from client and returns requested files
    def listen(self):
        self.sock.listen(5)

        while True:
            # Accepts connection
            clientSock, clientAddr = self.sock.accept()
            # Get the message
            while True:
                # Handles error of user entering a query that isn't an ASCII value
                try:
                    query = clientSock.recv(1024).decode("ascii")
                    if len(query)>=3 and query[-2:] == "\r\n":
                        query = query[0:-2]
                except UnicodeDecodeError as e:
                    clientSock.sendall(("Invalid input.").encode("ascii"))
                    break
                
                # Handles illformated requests
                if not len(query):
                    break
                elif len(query) >= 255:
                    clientSock.sendall(("Please limit selector string to 255 characters, thanks.").encode("ascii"))
                # Returns directory contents if requested
                elif (query == "." or query == "\r\n" or query == "\n"):
                    file = open("Content/.links", "r")
                    responseText = self.formatResponseFile(file)
                    clientSock.sendall(responseText.encode("ascii"))
                else:
                    queryPathParts = self.splitQuery(query)
                    file = self.openDestinationFileOrDirectory(queryPathParts, clientSock)
                    if file:
                        textResponse = self.formatResponseFile(file)
                        clientSock.sendall(textResponse.encode("ascii"))
                # Should we break everytime?
                break
            clientSock.close()
            
    
def main():
    # Create a server
    if len(sys.argv) > 1:
        try:
            server = TCPServer(int(sys.argv[1]))
        except ValueError as e:
            print ("Error in specifying port. Creating server on default port.")
            server = TCPServer()
    else:
        server = TCPServer()

    # Listening on port 50000
    server.listen()

main()