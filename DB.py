#!/usr/bin/env python

"""
Created by _UserName_
11/28/2013
"""

import sqlite3

class DB():
    def __init__(self):
        self.__databaseName = "database.db"
    def __call__(self):
        return self
    
    ###############################################################################
    
    def manager(self):
        conn = sqlite3.connect(self.__databaseName)
        c    = conn.cursor()
        
        c.execute("SELECT * FROM self")
        print "Table: self"
        while True:
            data = c.fetchone()
            if(data == None):
                break
            print "\t" + data[0] + "\t" + data[1]
        
        c.execute("SELECT * FROM peers")
        print "Table: peers"
        while True:
            data = c.fetchone()
            if(data == None):
                break
            print "\t" + data[0] + "\t" + data[1]
        
        conn.close()
    
    
    ###############################################################################
    
    """
    Database:
        self
            ident
            externIP
        peers
            peer_id
            peer_ip
    """
    def create(self):
        conn = sqlite3.connect(self.__databaseName)
        c    = conn.cursor()
        
        c.execute("CREATE TABLE self (ident, externIP)")
        c.execute("CREATE TABLE peers (peer_id, peer_ip)")
        
        conn.commit()
        conn.close()
    
    ###############################################################################
    
    def personalInfo(self, ident, externIP):
        conn = sqlite3.connect(self.__databaseName)
        c    = conn.cursor()
        
        c.execute("INSERT INTO self VALUES (?, ?)", (ident, externIP))
        
        conn.commit()
        conn.close()
        
    def getIdent(self):
        conn = sqlite3.connect(self.__databaseName)
        c    = conn.cursor()
        
        c.execute("SELECT ident FROM self LIMIT 0, 1")
        ident = c.fetchone()
        
        conn.close()
        
        return ident[0]
    
    def getExternIP(self):
        conn = sqlite3.connect(self.__databaseName)
        c    = conn.cursor()
        
        c.execute("SELECT externIP FROM self LIMIT 0, 1")
        
        conn.commit()
        conn.close()
    
    def updateExternIP(self, externIP):
        conn = sqlite3.connect(self.__databaseName)
        c    = conn.cursor()
        
        c.execute("UPDATE self SET externIP=? WHERE ident=(SELECT ident FROM self LIMIT 0, 1)", (externIP))
        
        conn.commit()
        conn.close()
    
    ###############################################################################
    
    def addPeer(self, peer_id, peer_ip):
        conn = sqlite3.connect(self.__databaseName)
        c    = conn.cursor()
        
        c.execute("INSERT INTO peers VALUES (?, ?)", (peer_id, peer_ip))
        
        conn.commit()
        conn.close()
    
    def findPeer(self, peer_id):
        conn = sqlite3.connect(self.__databaseName)
        c = conn.cursor()
        
        peers = []
        
        # Should create a 2d array: [[peer_id1, peer_ip], [peer_id2, peer_ip2]]
        c.execute("SELECT * FROM peers WHERE peer_id=(?)", (peer_id,))
        
        while True:
            peer = c.fetchone()
            if(peer == None):
                break
            else:
                peers.append(peer)
        
        conn.close()
        
        return peers
    
    def getAllPeers(self):
        conn = sqlite3.connect(self.__databaseName)
        c = conn.cursor()
        
        peers = []
        
        # Should create a 2d array: [[peer_id1, peer_ip], [peer_id2, peer_ip2]]
        c.execute("SELECT * FROM peers")
        
        while True:
            peer = c.fetchone()
            if(peer == None):
                break
            else:
                peers.append(peer)
        
        conn.close()
        
        return peers
