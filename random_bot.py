import random
from BBOAPI.app import interface

def bidFn(maxBid, bidLst):
    return maxBid+1

def playFn():
    pass

interface(bidFn, playFn)