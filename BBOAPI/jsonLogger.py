import json
import method

class jsonLogger():
    def __init__(self):
        self.logRecord = []
        self.print = True

    def initRoundLog(self):
        self.logRecord.append({
            'cardPoints': [],
            'cardsBySuit': [],
            'bid': [],
            'contract': "",
            'dealer': 0,
            'lastScore': 0,
            'trump': 0,
            'play': [],
            'scoreGot': 0,
            'score': 0
        })

    def record(self, attribute, data, round=0):
        if data==None:
            self.logRecord[round-1][attribute]=self.logRecord[round-2][attribute]
        else:
            self.logRecord[round-1][attribute]=data
        if self.print:
            print(attribute, data)
    
    def push(self, attribute, data, round=0):
        self.logRecord[round-1][attribute].append(data)
        if self.print:
            print(attribute, data)

    def get(self, attribute, round=0):
        return self.logRecord[round-1][attribute]

    def rounds(self):
        return len(self.logRecord)
    
    def close(self):
        with open("logs/"+method.timeStr()+".json", "a",encoding='utf8',errors='ignore') as f:
            json.dump(self.logRecord, f, ensure_ascii=False, indent=4)