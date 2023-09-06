def cardPointCount(deck):
    threshold = 10-2
    result = [0, 0, 0, 0]
    for i in deck:
        if i%13 > threshold:
            result[i//13]+=i%13-threshold
    return result

def cardsBySuit(deck):
    result = [0, 0, 0, 0]
    for i in deck:
        result[i//13]+=1
    return result

def bidClassify(firstBidder, bidLst):
    result = [ [] for i in range(4)]
    for i in range(len(bidLst)):
        result[(firstBidder+i)%4].append(bidLst[i])
    return result