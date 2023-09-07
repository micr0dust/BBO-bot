import sys, time

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("logs/"+self.timeStr()+".log", "a",encoding='utf8',errors='ignore')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass    

    def timeStr(self):
        now = time.localtime(time.time())
        return ("%s-%s-%s %s-%s-%s" %
            (now.tm_year,
            now.tm_mon,
            now.tm_mday,
            now.tm_hour,
            now.tm_min,
            now.tm_sec))

    def close(self):
        print('****************程式結束********************')
        self.log.close()

def close():
    sys.stdout.close()

sys.stdout = Logger()
