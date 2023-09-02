import random
from BBOAPI.app import agent
import BBOAPI.mapping as mapping

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
    print("王牌：", mapping.numToSuit[data['king']])

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

agent("withBots", bidFn, beforePlayFn, playFn, bidEndFn, roundEndFn, gameEnd)