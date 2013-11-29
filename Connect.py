#!/usr/bin/env python

"""
Created by _UserName_
11/28/2013
"""

import socket, md5, threading
import DB

class Connect():
    def __init__(self, IP):
        self.__port = 4444
        self.__host = (IP, self.__port)
        
        self.__databaseName = "database.db"
        
        # Generate Ident
        self.__database = DB.DB()
        self.__ident = self.__database.getIdent()
        
        # Length Of Packet
        self.__bufferLengthKB = 4
        self.__bufferLength   = 1024 * self.__bufferLengthKB
    def __call__(self):
        return self
    
    ######################################################################
    
    """
    Packet Composition:
        (MD5 Of Inner) | [(Ident Of Self) |(Message)]
    """
    
    """
    Returns:
        None      : Message Corrupted
        2 Strings : Peer's ID, Message
    """
    def __analyzePacket(self, packet):
        inner    = packet[32:]
        md5_comp = packet[:32]
        
        m = md5.new()
        m.update(inner)
        check = m.digest().encode('hex')
    
        if(check == md5_comp):
            # Message Has No Data Loss
            #         ID        Message
            return inner[:32], inner[32:]
        else:
            # Message Corrupted
            return None, None
    
    """
    Returns:
        None   : Packet Length Is To Large
        String : The Packet
    """
    def __generatePacket(self, data):
        packet = ""
        inner = self.__ident + data
        
        # Generate MD5 Of inner
        # Length = 32
        md = md5.new()
        md.update(inner)
        innerMD5 = md.digest().encode('hex')
        
        packet = innerMD5 + inner
        
        if(len(packet) > self.__bufferLength):
            return None
        else:
            return packet
    
    ######################################################################
    
    def startListener(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        server.bind((self.__host))
        server.listen(5)
        
        try:
            while True:
                try:
                    client, addr = server.accept()
                    
                    peer_name = str(client.getpeername()[0])
                    print 'Connection From: ' + peer_name
                    
                    client.send(self.__generatePacket("Connection Successful"))
                    self.__comWithPeer(client)
                except Exception, e:
                    #print e
                    pass
            server.close()
        except Exception, e:
            #print "startListener" + str(e)
            pass
    
    ######################################################################
    
    def connectToPeer(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(30)
            sock.connect(self.__host)
            
            self.__comWithPeer(sock)
            
            return 0
        except Exception, e:
            #print "connectToPeer" + str(e)
            return -1
    
    ######################################################################
    
    def __analyzeMessage(self, mess):
        """
        Possible Commands To Have While Connected:
            File Transfer
            Close Connection
        """
        mess = mess.lower()
        
        if((mess.find("/exit") >= 0) or (mess.find("/quit") >= 0)):
            return -1
        else:
            return 0
    
    def __recvFromPeer(self, sock):
        try:
            peer_known = False
            
            while True:
                raw_packet    = sock.recv(self.__bufferLength)
                peer_id, mess = self.__analyzePacket(raw_packet)
                
                if(mess == None):
                    pass
                
                elif(peer_known == False):
                    a = str(peer_id)
                    if(self.__database.findPeer(a) == []):
                        # Peer Not In DB
                        self.__database.addPeer(a, sock.getpeername()[0])
                    peer_known = True
                
                else:
                    print "<" + peer_id + "> " + mess
        except socket.timeout:
            print '[-] Socket Timed-out'
            sock.close()
            return -1
        except socket.errno:
            print '[-] Socket Error'
            return -1
        except Exception, e:
            #print "__recvFromPeer" + str(e)
            return -1
    
    def __comWithPeer(self, sock):
        threading.Thread(target=self.__recvFromPeer, args=(sock,)).start()
        
        try:
            while True:
                mess  = raw_input("")
                analy = self.__analyzeMessage(mess)
                
                if(analy == -1):
                    sock.close()
                elif(analy == 0):
                    packet = self.__generatePacket(mess)
                    calculate
                    sock.send(packet)
                
        except socket.timeout:
            print '[-] Socket Timed-out'
            sock.close()
            return -1
        except socket.errno:
            print '[-] Socket Error'
            return -1
        except Exception, e:
            #print "__comWithPeer" + str(e)
            return -1
