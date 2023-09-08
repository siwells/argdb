#!/usr/bin/python

import json
import sqlite3

import sadface as sf

from . import config

db = None

def cleanup():
    """

    """
    print("Cleaning up.")
    db.close()
    print("Stopping ArgDB...")
    exit(1)


def add_doc(new_doc):
    """

    """
    #TODO: Verify document

    cursor = db.cursor()
    cursor.execute("INSERT INTO raw (id, data) VALUES (NULL,json('"+new_doc+"') );")
    db.commit()


def init(config_pathname=None):
    """
    Initialises ArgDB. If a configuration file is supplied then that is used
    otherwise a default configuration is generated and saved to the working
    directory in which ArgDB was initiated.
    """
    if config_pathname is None:
        config.generate_default()
        config_pathname = config.get_config_name()

    current_config = config.load(config_pathname)
    
    global db
    dbname = config.current.get('datastore', "name")

    db = sqlite3.connect(dbname+'.sqlite3')

    cur = db.cursor()
    
    cur.executescript('''
        CREATE TABLE IF NOT EXISTS raw (
        id   INTEGER PRIMARY KEY,
        data JSON);
        ''')

    db.commit()



