import time
import threading
import socket
import gps

class GpsController(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.gpsstring = 'No GPS Fix'
    self.running = True #setting the thread running to true

  def run(self):
    session = None
    connected = False

    while self.running:
        while not connected and self.running:
            try:
                session = gps.gps("localhost", "19000")
                connected = True
            except socket.error:
                time.sleep(2)

        session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

        for report in session:
            if not self.running:
                    break
                    
            if session.fix.mode > 2:
                self.gpsstring = 'lat %.5f, lon %.5f %.1fmph' % (session.fix.latitude, session.fix.longitude, session.fix.speed * 2.23694)
            else:
                self.gpsstring = 'No GPS Fix'
                
            time.sleep(0.25)            

        connected = False
        self.gpsstring = 'No GPS Fix'
        time.sleep(2)