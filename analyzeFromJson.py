import json
import matplotlib.pyplot as plt

def scoreAccPlt(datas, files):
    for data in datas:
        plt.plot([0]+[i['score'] for i in data])
    plt.xticks([])
    plt.ylabel('score')
    plt.xlabel('round')
    plt.title("Acc Score")
    plt.legend(files, loc='best')
    plt.show()

def main():
    files = ["natureBid","randomBid"]
    datas = []
    for file in files:
        f = open("logs/"+file+".json","r",encoding="utf-8")
        data = json.loads(f.read())
        datas.append(data['data'])
    scoreAccPlt(datas, files)
main()