import random
from BBOAPI.app import agent
import BBOAPI.mapping as mapping
import BBOAPI.jsonLogger as jsonLog
import method

logEnable = True


jlog = jsonLog.jsonLogger()
if logEnable:
    import BBOAPI.loger as log

def beforeBidFn(deck):
    jlog.initRoundLog()
    print("=====第 "+str(jlog.rounds())+" 局================")
    jlog.record('cardPoints', method.cardPointCount(deck))
    jlog.record('cardsBySuit', method.cardsBySuit(deck))

def natureBidFn(data):
    cardPoints = jlog.get('cardPoints')
    cardsBySuit = jlog.get('cardsBySuit')
    print("now bid:",data['bidLst'], "max bid:", mapping.idToAction[data['maxBid'] if data['maxBid'] >= 0 else 35])
    trybid = mapping.bidToId['Pass']
    pointSum = sum(cardPoints)
    bidsClassify = method.bidClassify(data['rounds'], list(map(mapping.bidToId.get, data['bidLst'])))
    teammateBid = method.maxBidVal(bidsClassify[1])
    myBid = method.maxBidVal(bidsClassify[3])
    # 答叫
    if teammateBid != -1:
        # 1線高花答叫
        if teammateBid==mapping.bidToId['1♠'] or teammateBid==mapping.bidToId['1♥']:
            if teammateBid==mapping.bidToId['1♠'] and cardsBySuit[3] >= 3:
                if pointSum >= 12:
                    trybid=mapping.bidToId['4♠']
                elif pointSum >= 10:
                    trybid=mapping.bidToId['3♠']
                elif pointSum >= 4:
                    trybid=mapping.bidToId['2♠']
            elif teammateBid==mapping.bidToId['1♥'] and cardsBySuit[2] >= 3:
                if pointSum >= 12:
                    trybid=mapping.bidToId['4♥']
                elif pointSum >= 10:
                    trybid=mapping.bidToId['3♥']
                elif pointSum >= 4:
                    trybid=mapping.bidToId['2♥']
                elif cardsBySuit[3] >= 4 and pointSum >= 5:
                    trybid=mapping.bidToId['1♠']
            if trybid == mapping.bidToId['Pass']:
                if pointSum >= 13:
                    trybid=mapping.bidToId['3NT']
                elif pointSum >= 11:
                    trybid=mapping.bidToId['2NT']
                elif pointSum >= 5:
                    trybid=mapping.bidToId['1NT']
        # 1線低花答叫
        elif teammateBid < mapping.bidToId['1♥']:
            if (cardsBySuit[3] >= 4 or cardsBySuit[2] >= 4) and pointSum >=5:
                if cardsBySuit[3] == cardsBySuit[2] and cardsBySuit[2]==4:
                    trybid=mapping.bidToId['1♥']
                elif cardsBySuit[3] == cardsBySuit[2] and cardsBySuit[2]==5:
                    trybid=mapping.bidToId['1♠']
                elif cardsBySuit[3] >= cardsBySuit[2]:
                    trybid=mapping.bidToId['1♠']
                elif cardsBySuit[2] > cardsBySuit[3]:
                    trybid=mapping.bidToId['1♥']
            else:
                if pointSum >= 13:
                    trybid=mapping.bidToId['3NT']
                elif pointSum >= 11:
                    if cardsBySuit[0] >= 5 or cardsBySuit[1] >= 5:
                        if cardsBySuit[0] >= cardsBySuit[1]:
                            trybid=mapping.bidToId['3♣']
                        else:
                            trybid=mapping.bidToId['3♦']
                    else:
                        trybid=mapping.bidToId['2NT']
                elif pointSum >= 5:
                    if cardsBySuit[0] >= 4 or cardsBySuit[1] >= 4:
                        if cardsBySuit[0] >= cardsBySuit[1]:
                            trybid=mapping.bidToId['2♣']
                        else:
                            trybid=mapping.bidToId['2♦']
                    else:
                        trybid=mapping.bidToId['1NT']
    # 開叫人再叫
    elif teammateBid != -1 and myBid != -1:
        # 2線再叫
        if teammateBid >= mapping.bidToId['2♣'] and teammateBid <= mapping.bidToId['2♠']:
            if pointSum >= 19:
                if teammateBid == mapping.bidToId['2♠']:
                    trybid=mapping.bidToId['4♠']
                elif teammateBid == mapping.bidToId['2♥']:
                    trybid=mapping.bidToId['4♥']
                else:
                    trybid=mapping.bidToId['3NT']
            elif pointSum >= 16:
                if teammateBid == mapping.bidToId['2♠']:
                    trybid=mapping.bidToId['3♠']
                elif teammateBid == mapping.bidToId['2♥']:
                    trybid=mapping.bidToId['3♥']
                elif teammateBid == mapping.bidToId['2♦'] and cardsBySuit[1]>=4:
                    trybid=mapping.bidToId['3♦']
                elif teammateBid == mapping.bidToId['2♣'] and cardsBySuit[0]>=4:
                    trybid=mapping.bidToId['3♣']
                else:
                    trybid=mapping.bidToId['2NT']
        # 3線再叫
        elif teammateBid >= mapping.bidToId['3♣'] and\
            teammateBid <= mapping.bidToId['3♠'] and\
            pointSum >= 12:
            if cardsBySuit[3] >= 4:
                trybid=mapping.bidToId['4♠']
            elif cardsBySuit[2] >= 4:
                trybid=mapping.bidToId['4♥']
            elif cardsBySuit[2] >= 4 or cardsBySuit[2] >= 4:
                trybid=mapping.bidToId['3NT']
        # 1線高花再叫
        elif teammateBid <= mapping.bidToId['1♠']:
            if teammateBid == mapping.bidToId['1♥']:
                if pointSum >= 19:
                    if cardsBySuit[2] >= 4:
                        trybid=mapping.bidToId['4♥']
                    elif cardsBySuit[3] >= 4:
                        trybid=mapping.bidToId['1♠']
                    else:
                        trybid=mapping.bidToId['3NT']
                elif pointSum >= 16:
                    if cardsBySuit[2] >= 4:
                        trybid=mapping.bidToId['3♥']
                    elif cardsBySuit[3] >= 4:
                        trybid=mapping.bidToId['1♠']
                    elif myBid == mapping.bidToId['1♣'] and cardsBySuit[0]>=6:
                        trybid=mapping.bidToId['3♣']
                    elif myBid == mapping.bidToId['1♦'] and cardsBySuit[1]>=6:
                        trybid=mapping.bidToId['3♦']
                    else:
                        trybid=mapping.bidToId['2NT']
                elif pointSum >= 12:
                    if cardsBySuit[2] >= 4:
                        trybid=mapping.bidToId['2♥']
                    elif cardsBySuit[3] >= 4:
                        trybid=mapping.bidToId['1♠']
                    elif myBid == mapping.bidToId['1♣'] and cardsBySuit[0]>=6:
                        trybid=mapping.bidToId['2♣']
                    elif myBid == mapping.bidToId['1♦'] and cardsBySuit[1]>=6:
                        trybid=mapping.bidToId['2♦']
                    else:
                        trybid=mapping.bidToId['1NT']
            elif teammateBid == mapping.bidToId['1♠']:
                if pointSum >= 19:
                    if cardsBySuit[3] >= 4:
                        trybid=mapping.bidToId['4♠']
                    else:
                        trybid=mapping.bidToId['3NT']
                elif pointSum >= 16:
                    if cardsBySuit[2] >= 4:
                        trybid=mapping.bidToId['3♠']
                    elif myBid == mapping.bidToId['1♥'] and cardsBySuit[2]>=6:
                        trybid=mapping.bidToId['3♥']
                    elif myBid == mapping.bidToId['1♣'] and cardsBySuit[0]>=6:
                        trybid=mapping.bidToId['3♣']
                    elif myBid == mapping.bidToId['1♦'] and cardsBySuit[1]>=6:
                        trybid=mapping.bidToId['3♦']
                    else:
                        trybid=mapping.bidToId['2NT']
                elif pointSum >= 12:
                    if cardsBySuit[2] >= 4:
                        trybid=mapping.bidToId['2♠']
                    elif myBid == mapping.bidToId['1♥'] and cardsBySuit[2]>=6:
                        trybid=mapping.bidToId['2♥']
                    elif myBid == mapping.bidToId['1♣'] and cardsBySuit[0]>=6:
                        trybid=mapping.bidToId['2♣']
                    elif myBid == mapping.bidToId['1♦'] and cardsBySuit[1]>=6:
                        trybid=mapping.bidToId['2♦']
                    else:
                        trybid=mapping.bidToId['1NT']
    # 開叫
    else:
        if pointSum > 21:
            trybid = mapping.bidToId['2♣']
        elif pointSum >= 12:
            if cardsBySuit[3] >= 5 and cardsBySuit[3]>=cardsBySuit[2]:
                trybid = mapping.bidToId['1♠']
            elif cardsBySuit[2] >= 5:
                trybid = mapping.bidToId['1♥']
            elif cardsBySuit[1] > cardsBySuit[0]:
                trybid = mapping.bidToId['1♦']
            elif cardsBySuit[1] == cardsBySuit[0]:
                if cardsBySuit[0] >= 4:
                    trybid = mapping.bidToId['1♦']
                else: trybid = mapping.bidToId['1♣']
            else: trybid = mapping.bidToId['1♣']

    return trybid if trybid>data['maxBid'] else 35

def bidFn(data):
    # return 35
    print(data['bidLst'])
    bid = data['maxBid']+1\
         if random.randint(0,1) else 35
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
    suit = int((data['table'][0])/13) if len(data['table']) else -1
    deck = data[data['turn']]
    candidates = list(filter(lambda x:int(x/13)==suit, deck))
    if len(candidates)==0:
        candidates=deck
    return candidates[random.randint(0,len(candidates)-1)]

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
    agent("withBots", 40, beforeBidFn, natureBidFn, bidEndFn, beforePlayFn, playFn, roundEndFn, gameEnd)
    
try:
    main()
    jlog.close()
    if logEnable:
        log.close()
    print("end")
except KeyboardInterrupt:
    jlog.close()
    if logEnable:
        log.close()