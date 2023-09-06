import random
from BBOAPI.app import agent
import BBOAPI.mapping as mapping
import BBOAPI.logging as log
import method

logEnable = True
cardPoints = []
cardsBySuit = []

def beforeBidFn(deck):
    global cardPoints, cardsBySuit
    cardPoints = method.cardPointCount(deck)
    print("牌力", cardPoints)
    cardsBySuit = method.cardsBySuit(deck)
    print("各花色卡牌數", cardsBySuit)

def natureBidFn(data):
    trybid = 35
    pointSum = sum(cardPoints)
    bidsClassify = method.bidClassify(data['rounds'], data['bidLst'])
    # print(list(map(lambda x: map(lambda y:mapping.idToAction[y]), bidsClassify)))
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
    print("叫牌紀錄：", data)
    print("===== 叫牌結束 ===================")

def beforePlayFn(data):
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
    print("打牌: ",list(map(lambda x: mapping.valToCard[x], data['table'])),
            "最大: ", mapping.valToCard[data['table'][data['maxIdx']]])

def gameEnd(data):
    print("-------第 "+str(data['round'])+" 局結束，目前為" + str(data['score']) + " 分-------")

def main():
    agent("withBots", beforeBidFn, natureBidFn, bidEndFn, beforePlayFn, playFn, roundEndFn, gameEnd)

try:
    main()
except:
    log.close()