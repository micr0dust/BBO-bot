import json
import matplotlib.pyplot as plt

def plotScore(lst, ylabel, xlabel, title):
    plt.plot(lst, color='magenta', marker='o',mfc='pink' )
    plt.xticks(range(1,len(lst)+1, 1))
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.show()

def scoreAccPlt(data):
    plotScore([0]+[i['score'] for i in data],'score','round',"Acc Score")

def main():
    f = open("logs/"+input(),"r",encoding="utf-8")
    data = json.loads(f.read())
    scoreAccPlt(data)
    print([i['score'] for i in data])
main()