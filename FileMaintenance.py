import time
import os
import threading

class FileMaintenance(threading.Thread):
  def __init__(self, dir):
    threading.Thread.__init__(self)
    self.running = True 
    self.dir = dir

  def run(self):
    while self.running:
        for i in range(59):
            time.sleep(1)
            if not self.running:
                break
                
        while self.running and DirectorySize(self.dir + '/') > 4194304000:            
            files = os.listdir(self.dir)
            files.sort()
            if len(files) > 1:               
                os.remove(self.dir + '/' + files.pop(0))
            time.sleep(5)
        
def DirectorySize(dir):
    return sum(os.path.getsize(dir + f) for f in os.listdir(dir))