import random
from BBOAPI.app import agent
import BBOAPI.mapping as mapping
import method
import json

logRecord = []

logEnable = True

if logEnable:
    import BBOAPI.loger as log

def initRoundLog():
    global logRecord
    logRecord.append({
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

def beforeBidFn(deck):
    global logRecord
    initRoundLog()
    logRecord[-1]['cardPoints'] = method.cardPointCount(deck)
    logRecord[-1]['cardsBySuit'] = method.cardsBySuit(deck)
    print("牌力", logRecord[-1]['cardPoints'])
    print("各花色卡牌數", logRecord[-1]['cardsBySuit'])

def natureBidFn(data):
    global logRecord
    cardPoints = logRecord[-1]['cardPoints']
    cardsBySuit = logRecord[-1]['cardsBySuit']
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
    global logRecord
    logRecord[-1]['bid']=data
    print("叫牌紀錄：", data)
    print("===== 叫牌結束 ===================")

def beforePlayFn(data):
    global logRecord
    logRecord[-1]['contract']=data['contract']
    logRecord[-1]['dealer']=int(data['dealer'])
    logRecord[-1]['lastScore']=int(data['score'])
    logRecord[-1]['trump']=int(data['trump'])
    
    print("叫牌結果：", data['contract'])
    print("莊家：", mapping.numToTeamName[data['dealer']])
    print("分數：", data['score'])
    print("王牌：", mapping.numToSuit[data['trump']])

def playFn(data):
    suit = int((data['table'][0])/13) if len(data['table']) else -1
    deck = data[data['turn']]
    candidates = list(filter(lambda x:int(x/13)==suit, deck))
    if len(candidates)==0:
        candidates=deck
    return candidates[random.randint(0,len(candidates)-1)]

def roundEndFn(data):
    global logRecord
    logRecord[-1]['play'].append({
        'table': data['table'],
        'max': data['table'][data['maxIdx']],
        'winner': data['maxIdx']
    })
    print("打牌: ",list(map(lambda x: mapping.valToCard[x], data['table'])),
            "最大: ", mapping.valToCard[data['table'][data['maxIdx']]])

def gameEnd(data):
    global logRecord
    logRecord[-1]['score']=int(data['score'])
    logRecord[-1]['scoreGot']=logRecord[-1]['score']-logRecord[-1]['lastScore']
    print("-------第 "+str(data['round'])+" 局結束，目前為" + str(data['score']) + " 分-------")

def main():
    agent("withBots", 40, beforeBidFn, natureBidFn, bidEndFn, beforePlayFn, playFn, roundEndFn, gameEnd)

try:
    main()
except KeyboardInterrupt:
    with open("logs/"+method.timeStr()+".json", "a",encoding='utf8',errors='ignore') as f:
        json.dump(logRecord, f, ensure_ascii=False, indent=4)
    if logEnable:
        log.close()