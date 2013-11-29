#!/usr/bin/env python

"""
Created by _UserName_
11/28/2013
"""

import Connect, DB
import uuid

def Register():
    # Generate A Unique Idenfifier
    ident = uuid.uuid4().hex
    
    # Allow For Database Manipulation
    database = DB.DB()
    
    # Create Database
    database.create()
    
    # Add Self To Database
    externalIP = "127.0.0.1"
    database.personalInfo(ident, externalIP)
