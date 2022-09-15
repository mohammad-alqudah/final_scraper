
from datetime import datetime

def last_update(channel):
    
    channel.last_update =datetime.now()
    channel.save()
     