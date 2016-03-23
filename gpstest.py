import gps

session = gps.gps("localhost", "19000")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

for report in session:
    if session.fix.mode > 2:
        print '%.5f %.5f %.1fmph' % (session.fix.latitude, session.fix.longitude, session.fix.speed * 2.23694)        
    else:
        print 'No Fix'