Computer Networks Final Assignment - Spring 2018

Authors: Emilee F, Malcolm M, Steph H
Credit to : Amy Csizmar Dalal for Sockets Lab starter file
Date:  12 April 2018

Assignment: 1991 Gopher Internet Protocol implementation - Client and Server
RFC 1436: https://tools.ietf.org/html/rfc1436

------
Final Modifications we made:

CLIENT:
fixed hanging client by adding '/r/n'
  > connects to other servers now yay!
Fails gracefully (always) when connecting to external servers
Added numbers to user interface and changed informational line to improve usability and user-interactions.


SERVER:
added code to remove '/r/n' at the end of query
