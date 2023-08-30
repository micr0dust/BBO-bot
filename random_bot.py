import random
from BBOAPI.app import agent

def bidFn(maxBid, bidLst):
    # return 35
    return maxBid+1\
         if random.randint(0,1) else 35

def playFn(data):
    suit = int((data['table'][0])/13) if len(data['table']) else -1
    deck = data[data['turn']]
    candidates = list(filter(lambda x:int(x/13)==suit, deck))
    if len(candidates)==0:
        candidates=deck
    return candidates[random.randint(0,len(candidates)-1)]

agent("withBots", bidFn, playFn)