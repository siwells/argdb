#!/usr/bin/python

from configparser import ConfigParser
import json
import os

from . import utils

current = None
config_pathname = None

def generate():
    """
    Create a new default configuration file
    """
    global config_pathname
    config_pathname = 'default.cfg'
    
    if not os.path.exists(config_pathname):
        cp = ConfigParser()
        cp['datastores'] = {'names':['default'],'types':['tinydb', 'couchdb'] }
        cp['default'] = {'type': 'tinydb'}
        cp.write(open('default.cfg', 'w'))
    

def load(pathname=None):
    """
    Load a configuration file
    """
    if(pathname is not None):
        try:
            global current, config_pathname
            config_pathname = pathname
            current = ConfigParser()
            current.read(pathname)
            return current
        except:
            print("Could not read configs from " + pathname)
            exit(1) 
    else:
        raise Exception("Tried to load config file but pathname (location) was set to None")
        exit(1)

def add_datastore_config_entry(db_name, db_type):
    """
    Add a new datastore entry to the in memory config & persist changes to disk

    A datastore entry comprises an entry in the list of datastore names and an associated
    named section in the body of the config where the name of the section matches the name
    entered in the list of datastores. This way we can easily retrieve a list of datastores
    which enables us to process the rest of the configuration.
    """
    global current, config_pathname
    conf = current

    datastores = utils.rectify(conf.get('datastores','names'))
    
    if db_name not in datastores:
        datastores.append(db_name)
        conf['datastores']['names'] = json.dumps(datastores)
        conf[db_name] = {'type': db_type}
        
        with open(config_pathname, 'w') as config_file:
            conf.write(config_file)

        current = conf
        return True

def remove_datastore_config_entry(db_name):
    """
    Removes the configuration entry for a given datastore.
    """
    global current, config_pathname
    conf = current

    datastores = utils.rectify(conf.get('datastores','names'))
    if db_name in datastores:
        datastores.remove(db_name)
        conf['datastores']['names'] = json.dumps(datastores)
        conf.remove_section(db_name)

        with open(config_pathname, 'w') as cfile:
            conf.write(cfile)

        current = conf
   
