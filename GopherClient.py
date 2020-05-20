'''
Gopher protocol implementation - Client
Authors: Emilee F, Malcolm M, Steph H
Credit to : Amy Csizmar Dalal for Sockets Lab starter file
CS 331, Spring 2018
Date:  12 April 2018
'''
import sys, socket

def usage():
    print ("Usage:  python GopherServer.py <server IP> 50000")

# Formats inputted file to specifications and returns its text
def formatLinksFile(text):
    # Limits line length to 70 characters
    lines = text.split("\n")
    newLines = lines
    for i in range(len(lines)):
        line = lines[i].split("\t")
        if len(line) < 3:
            return text
        if line[0][0] == "1":
            thisLine = str(i+1) + "   " + line[0][1:] + "..."
        else:
            thisLine = str(i+1) + "   " + line[0][1:]
        
        newLines[i] = thisLine

    text = "\n".join(newLines)

    return text

# Puts the contents of the links file into a dictionary
# Key = user display string, Value = file/directory name
def convertLinksToDictionary(links):
    lines = links.split("\n")
    dictionary = {}
    for i in range(len(lines)):
        line = lines[i].split("\t")
        if len(line) < 3:
            return {}
        key = str(i+1)
        value = line[1]
        dictionary[key] = value
        
    return dictionary

# Converts query to complete file path
def updateQuery(query, currentLocation):
    if currentLocation != "":
        query = currentLocation + query
        
    if query != None and query != "" and (query[-1] == "/" or query == "."):
        if query != ".":
            currentLocation = query
        
    return query, currentLocation

# Formats server response for display and updates current directory
def formatServerResponse(returned, currentLinksFileDictionary):
    returned = returned[:-2]
    #if isFolder:
    currentLinksFileDictionary = convertLinksToDictionary(returned)
    returned = formatLinksFile(returned)
    return returned, currentLinksFileDictionary

# Establishes and maintains connection with server
def speak(server, port):
    # Current directory location
    currentLocation = ""
    # Current directory (user display string to file name) dictionary
    currentLinksFileDictionary = {}
    # To account for user inputting an empty line
    print("Type ENTER or . for directory content. Type number on beginning of line to open respective file/folder. To close type ':q'")
    # Continues to run until client quits
    while True:
        # If user input is
        serverSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # Attempts to connect to server (fails gracefully)
        try: 
            serverSock.connect((server, port))
        except Exception as e:
            print("Connection Refused, please try again")
            return
        
        query = input()

        # Manages various user inputs
        if query == '' or query == '.':
            query = '.'
        elif query == ":q":
            break
        elif currentLinksFileDictionary != {} and query in currentLinksFileDictionary:
            query = currentLinksFileDictionary.get(query)
            query, currentLocation = updateQuery(query, currentLocation)

        # Connects to server
        print ("Connected to " + server + " at port " + str(port))
        query = query + "\r\n"
        serverSock.send(query.encode("ascii"))
        
        # Receives server reply, formats and displays
        returned = serverSock.recv(1024).decode("ascii")
        returned, newLinksDictionary = formatServerResponse(returned, currentLinksFileDictionary)
        print ("Received reply: ")
        print (returned)
        if newLinksDictionary != {}:
            currentLinksFileDictionary = newLinksDictionary
        
        # I think we can delete all the isFolder (possible)
        # Do we need more clear user interactions/interface
        # Work on ill formatted responses // gracefully fails

def main():
    # Process command line args (server, port, message)
    if len(sys.argv) == 3:
        try:
            server = sys.argv[1]
            port = int(sys.argv[2])
        except ValueError as e:
            usage()
        speak(server, port)
    else:
        usage()

main()