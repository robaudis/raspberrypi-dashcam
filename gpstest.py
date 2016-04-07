import gps
import time
import socket

session = None
connected = False

while True:
    while not connected:
        try:
            session = gps.gps("localhost", "19000")
            connected = True
        except socket.error:
            print 'GPSD not available, trying again'
            time.sleep(2)
        
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    for report in session:
        if session.fix.mode > 2:
            print '%.5f %.5f %.1fmph' % (session.fix.latitude, session.fix.longitude, session.fix.speed * 2.23694)        
        else:
            print 'No Fix'

    connected = False
    print 'GPSD connection lost - trying to reconnect'
    time.sleep(2)
    