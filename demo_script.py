'''
Created on 11/02/2014

@author: jrh
'''
from datetime import datetime

def format_time():
    return datetime.isoformat(datetime.utcnow())
