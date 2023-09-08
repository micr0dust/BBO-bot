import random
from BBOAPI.app import agent
import BBOAPI.mapping as mapping
import BBOAPI.jsonLogger as jsonLog
import functions.method as method
import functions as fn

logEnable = False


jlog = jsonLog.jsonLogger()
bidFunction = jlog.setFunction('bidFn', fn.bid.natureBid)
playFunction = jlog.setFunction('playFn', fn.play.randomPlay)

if logEnable:
    import BBOAPI.loger as log

def beforeBidFn(deck):
    jlog.initRoundLog()
    print("=====第 "+str(jlog.rounds())+" 局================")
    jlog.record('cardPoints', method.cardPointCount(deck))
    jlog.record('cardsBySuit', method.cardsBySuit(deck))

def bidFn(data):
    print("now bid:",data['bidLst'], "max bid:", mapping.idToAction[data['maxBid'] if data['maxBid'] >= 0 else 35])
    bid = bidFunction(data, jlog)
    print("My bid:", mapping.idToAction[bid])
    return bid

def bidEndFn(data):
    jlog.record('bid', data)
    print("===== 叫牌結束 ===================")

def beforePlayFn(data):
    jlog.record('contract', data['contract'])
    jlog.record('dealer', data['dealer'])
    jlog.record('lastScore', data['score'])
    jlog.record('trump', data['trump'])

def playFn(data):
    return playFunction(data, jlog)

def roundEndFn(data):
    jlog.push('play', {
        'table': data['table'],
        'max': data['table'][data['maxIdx']],
        'winner': data['maxIdx']
    })

def gameEnd(data):
    jlog.record('score', int(data['score']))
    jlog.record('scoreGot', jlog.get('score')-jlog.get('lastScore'))
    print("-------第 "+str(data['round'])+" 局結束，目前為" + str(data['score']) + " 分-------")

def main():
    try:
        agent("withBots", 40, beforeBidFn, bidFn, bidEndFn, beforePlayFn, playFn, roundEndFn, gameEnd)
        print("執行結束")
        jlog.close()
        if logEnable:
            log.close()
    except KeyboardInterrupt:
        print("中途結束")
        jlog.close()
        if logEnable:
            log.close()

main()
