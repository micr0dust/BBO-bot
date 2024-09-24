import random
import copy

# 每個人 n 張牌
n=3

allCards = list(range(4*n))
random.shuffle(allCards)
oneDeckLen = len(allCards)//4
decks = [
    allCards[:oneDeckLen],
    allCards[oneDeckLen:oneDeckLen*2],
    allCards[oneDeckLen*2:oneDeckLen*3],
    allCards[oneDeckLen*3:oneDeckLen*4]
]
# decks = [[13, 1, 3], [11, 7, 5], [12, 4, 2], [8, 6, 10]]
print(decks)
def minmax(decks, begin, table):
    res = -10000
    resLst = []
    ans = -1
    player=(begin+len(table))%4
    for i in range(len(decks[player])):
        tmp = copy.deepcopy(decks)
        tmp[player].pop(i)
        ret = None
        tmpLst = []
        if len(table)<3:
            ret, tmpLst = minmax(tmp, begin, table+[decks[player][i]])
            ret *= -1
        else:
            nowTable = table+[decks[player][i]]
            winner = (begin+nowTable.index(max(nowTable)))%4
            if len(tmp[winner]) == 0:
                return (1 if winner&1==player&1 else -1), [decks[player][i]]
            ret, tmpLst = minmax(tmp, winner, [])
            ret *= (1 if winner&1==player&1 else -1)
        if ret > res:
            res = ret
            ans = i
            resLst=tmpLst
    return res, resLst+[decks[player][ans]]
res,lst=minmax(decks, 0, [])
print(list(reversed(lst)))