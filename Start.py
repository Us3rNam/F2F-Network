#!/usr/bin/env python

"""
Created by _UserName_
11/28/2013
"""

import os, threading
import DB, Connect, Register

def main():
    databaseName = "database.db"
    
    if not (os.path.exists(databaseName)):
        Register.Register()
    
    shell()

def helpScreen():
    display = (
        "\t  Help\n" +
        " " * 3 + "-" * 18 + "\n" +
        "search\t\tFind peer by peer id (If blank show all known peers)\n" +
        "myid\t\tDisplays your id given to other peers\n" +
        "db_manager\tView all data in database\n" +
        "change_ip\tMust be your current external IP address\n" +
        "listen\t\tStart listening for connections\n" +
        "connect\t\tConnect to a peer\n" +
        " " * 3 + "-" * 18 + "\n" +
        "quit/exit\tExit the program\n" +
        "clear\t\tClears the screen\n" +
        "help\t\tShow this screen"
    )
    print display

def shell():
    # Allow For DB Touching
    database = DB.DB()
    
    while True:
        try:
            com = raw_input("\n> ")
            com = com.lower()
            
            print "\n"
            
            if(com.find("help") >= 0):
                helpScreen()
            
            elif(com.find("clear") >= 0):
                print '\n' * 25
            
            elif(com.find("search") >= 0):
                peer_id = raw_input("Peer's ID: ")
                if(peer_id == ""):
                    peers = database.getAllPeers()
                else:
                    peers = database.findPeer(peer_id)
                print '\n\t\t\tID\t\t\tIP'
                if(peers != []):
                    for i in range(len(peers)):
                        print "\t" + peers[i][0] + " " + peers[i][1]
                    
            elif(com.find("myid") >= 0):
                print "Your ID: " + database.getIdent()
                
            elif(com.find("db_manager") >= 0):
                database.manager()
            
            elif(com.find("change_ip") >= 0):
                externIP = raw_input("External IP: ")
                database.updateExternIP(externIP)
            
            elif(com.find("listen") >= 0):
                # Start Listener
                print "[*] Waiting For Connections"
                listen = Connect.Connect("")
                listen.startListener()
            
            elif(com.find("connect") >= 0):
                IP = raw_input("Peer's IP: ")
                con = Connect.Connect(IP)
                con.connectToPeer()
            
            elif((com.find("quit") >= 0) or (com.find("exit") >= 0)):
                return
            
        except KeyboardInterrupt:
            print '[*] Please Exit Correctly Next Time'
            break
        #except Exception, e:
            #print "shell" + str(e)

if __name__ == '__main__':
    main()
