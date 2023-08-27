import os, time
import BBOAPI.mapping as mapping
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from dotenv import load_dotenv
from time import sleep

__all__ = [
    'agent',
]

load_dotenv()
account = os.getenv("ACCOUNT")
password = os.getenv("PASSWORD")

options = Options()
# 不開啟實體瀏覽器背景執行
# options.add_argument("--headless")
# 最大化視窗
options.add_argument("--start-maximized ")
# 無痕模式
options.add_argument("--incognito ")
# 不載入圖片
# options.add_argument('blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(options=options)

def getEleByStr(string, tags):
    element = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.XPATH, "//"+tags+"[contains(text(),'"+string+"')]"))
    )
    gameBtn = driver.find_element("xpath", "//"+tags+"[contains(text(),'"+string+"')]")
    return gameBtn

def getElesByStr(string, tags):
    element = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.XPATH, "//"+tags+"[contains(text(),'"+string+"')]"))
    )
    gameBtn = driver.find_elements("xpath", "//"+tags+"[contains(text(),'"+string+"')]")
    return gameBtn

def elementInfo(element):
    attrs = driver.execute_script('\
        var items = {};\
        for (index = 0; index < arguments[0].attributes.length; ++index) {\
            items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value };\
        return items;\
    ', element)
    print(attrs)

def error(msg):
    print(msg)
    driver.quit()

def getAllCards():
    cards = driver.find_elements(By.CSS_SELECTOR, ".gwt-Image")
    return cards[:-2]

def cardsFromNodes(lst):
    cards = driver.execute_script('\
            let result = [];\
            for (let img of arguments[0])\
                result.push(img.src.replace("data:image/png;base64,",""));\
            return result;\
        ', lst)
    return cards

def isMoving(element):
    current_location = element.location
    time.sleep(0.1)
    if current_location != element.location:
        return True
    return False

# from base64
def printCard(cards):
    import base64
    import io
    from matplotlib import pyplot as plt
    import matplotlib.image as mpimg
    fig = plt.figure(figsize=(6, 2))
    for i in range(len(cards)):
        img = mpimg.imread(io.BytesIO(base64.b64decode(cards[i])), format='PNG')
        fig.add_subplot(1, len(cards), i+1)
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(img)
    plt.show()

def deckValToStr(lst):
    return list(map(lambda x: mapping.valToCard[x], map(mapping.deck.get, lst)))

def realClick(element):
        # while driver.execute_script('return $("#northDeck > img").is(":animated");'):
        #     sleep(0.5)
        driver.execute_script('\
                let simulateMouseEvent = function(element, eventName, coordX, coordY) {\
                    element.dispatchEvent(new MouseEvent(eventName, {\
                        view: window,\
                        bubbles: true,\
                        cancelable: true,\
                        clientX: coordX,\
                        clientY: coordY,\
                        button: 0\
                    }));\
                };\
                \
                let theButton = arguments[0];\
                \
                let box = theButton.getBoundingClientRect(),\
                coordX = box.left + (box.right - box.left) / 2,\
                coordY = box.top + (box.bottom - box.top) / 2;\
                \
                simulateMouseEvent (theButton, "mousedown", coordX, coordY);\
                simulateMouseEvent (theButton, "mouseup", coordX, coordY);\
                simulateMouseEvent (theButton, "click", coordX, coordY);\
            ', element)

class Game:
    def __init__(self, mode):
        self.mode = mode

    def loginBBO(self):
        try:
            driver.implicitly_wait(20)
            nameIpt = driver.find_element(By.NAME, "username")
            driver.find_element(By.NAME, "username").send_keys(account)
            driver.find_element(By.NAME, "password").send_keys(password)
            loginDiv = driver.find_element(By.CSS_SELECTOR, '.footerLogin')
            loginBtn = loginDiv.find_element(By.TAG_NAME, "button")
            loginBtn.click()
        except:
            return False

        return True
    
    def playWithBot(self):
        driver.get("https://www.bridgebase.com/v3/")
        self.loginBBO()
        getEleByStr("紙牌遊戲", 'div').click()
        getEleByStr("只玩橋牌（免費）", 'div').click()
        getEleByStr(" 訊息 ", 'div').find_element("xpath", "../..").click()
        driver.implicitly_wait(5)
        iframe = driver.find_element(By.CSS_SELECTOR, ".iframeClass")
        wait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(iframe))

    def play(self):
        if self.mode=="withBots":
            self.playWithBot()

class Bidding:
    def __init__(self, bidFn):
        self.bidFn = bidFn

        driver.implicitly_wait(5)
        driver.find_element(By.CSS_SELECTOR, ".dvBigMode")
        driver.execute_script("document.querySelector('.dvBigMode').id='dvBigMode'")
        while not driver.execute_script("return document.getElementById('gameTable')"):
            sleep(0.1)
            table = driver.execute_script("\
            document.querySelector('.auctionBox').click();\
            let candidate = document.querySelector('.auctionBox').nextSibling;\
            while(candidate.classList.contains('callExplainPanel')) candidate=candidate.nextSibling;\
            candidate.id='gameTable';\
            console.log(document.querySelector('.auctionBox').nextSibling);")

    def getBid(self):
        result = driver.execute_script('\
            let table = document.querySelector("#BBO_mainDiv > div.dvBigMode > div.auctionBox > div > div > div");\
            let bids = table.getElementsByTagName("div");\
            let result = [];\
            for (let bid of bids)\
                result.push(bid.textContent);\
            return result;\
        ')
        return result

    def getActions(self):
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".biddingBoxPassButton")))
        sleep(0.5)
        driver.implicitly_wait(5)
        driver.find_element(By.CSS_SELECTOR, ".auctionBox")
        table = driver.execute_script("return document.querySelector('.auctionBox').nextSibling")
        btns = table.find_elements(By.TAG_NAME, "button")
        result = driver.execute_script('\
            let table = document.querySelector(".auctionBox").nextSibling;\
            let btns = table.getElementsByTagName("button");\
            let result = [];\
            for (let btn of btns)\
                result.push(btn.textContent);\
            return result;\
        ')
        action = {}
        for i in range(len(result)-2):
            action[result[i]]=i
        return action

    def bidAction(self, actions):
        print("my bid:" ,actions)
        driver.implicitly_wait(5)
        driver.find_element(By.ID, "gameTable")
        for action in actions:
            sleep(0.1)
            target = driver.execute_script('\
                let table = document.getElementById("gameTable");\
                let btns = table.getElementsByTagName("button");\
                for (let i=0; i<btns.length-2; i++)\
                    if(btns[i].textContent == arguments[0]){\
                        console.log(btns[i]);\
                        return btns[i];\
                    }\
            ', action)
            realClick(target)

    def maxBidVal(self, bidLst):
        return max(map(lambda x: x if x < mapping.bidToId["Pass"] else -1,
                        map(mapping.bidToId.get, bidLst)))

    def getDeck(self):
        cards = []
        while(len(cards) < 12):
            sleep(0.5)
            cards = cardsFromNodes(getAllCards())
        # printCard(cards)
        print(list(map(mapping.deck.get, cards)))
        print(deckValToStr(cards))
        return cards
        
    def startBid(self):
        print("wait...")
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".biddingBoxPassButton")))
        myDeck = self.getDeck()
        maxBid = -1
        bidding = True
        while(bidding):
            if not bidding:
                break
            bidLst = self.getBid()
            maxBid = self.maxBidVal(bidLst)
            print("now bid:",bidLst, "max bid:", mapping.idToAction[maxBid if maxBid >= 0 else 35])
            bid = self.bidFn(maxBid, bidLst)
            self.bidAction(mapping.idToAction[bid])
            print("wait...")
            try:
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".biddingBoxPassButton")))
            except:
                bidding = False
        return self.getBid()


class Playing:
    def __init__(self):
        cardsEle = driver.find_elements(By.CSS_SELECTOR, ".gwt-Image")
        south = cardsEle[0].find_element("xpath", "..")
        driver.execute_script("arguments[0].id='southDeck'", south)
        north = cardsEle[13].find_element("xpath", "..")
        driver.execute_script("arguments[0].id='northDeck'", north)
        driver.execute_script("\
            let bidRes = document.querySelector('.widgetPanel').querySelector('.contractPanel');\
            bidRes.querySelector('.gwt-HTML').id = 'contract';\
            bidRes.querySelector('.gwt-Label').id = 'dealer';\
            document.querySelector('.scorePanelTop').nextSibling.id = 'score';\
        ")
        self.dealer = -1
        self.leader = -1
        self.king = -1
        self.contract = ""

    def getDeck(self, name):
        # northDeck, southDeck
        cards = cardsFromNodes(driver.find_element(By.ID, name)
                                .find_elements(By.TAG_NAME, "img"))
        return cards if cards else []
    
    def getDeckNodes(self, name):
        # northDeck, southDeck
        return driver.find_element(By.ID, name).find_elements(By.TAG_NAME, "img")
    
    def getTableCards(self):
        return cardsFromNodes(getAllCards()[
            len(self.getDeck("southDeck"))+len(self.getDeck("northDeck")):
        ])
        # return cardsFromNodes(getAllCards()[
        #     len(self.getDeck("southDeck"))+len(self.getDeck("northDeck")):
        # ])
    # 最終叫牌結果(合約)
    def getContract(self):
        return driver.find_element(By.ID, "contract").text
    # 莊家
    def getDealer(self):
        return driver.find_element(By.ID, "dealer").text
    # 分數
    def getScore(self):
        return driver.find_element(By.ID, "score").text

    def kingSuit(self):
        if self.king >= 0:
            return self.king
        if "♣" in self.contract:
            self.king=0
        elif "♦" in self.contract:
            self.king=1
        elif "♥" in self.contract:
            self.king=2
        elif "♠" in self.contract:
            self.king=3
        elif "NT" in self.contract:
            self.king=4
        return self.king

    def playerNow(self, table=None):
        if table != None:
            return (self.leader+len(table))%4
        return (self.leader+len(self.getTableCards()))%4

    def waitForClick(self, info, idx):
        originLen = len(self.getDeckNodes(info['turn']))
        while len(self.getDeckNodes(info['turn'])) == originLen:
            realClick(self.getDeckNodes(info['turn'])[idx])
            sleep(0.5)

    def isEnd(self):
        return driver.find_element(By.CSS_SELECTOR, ".dealEndPanel").is_displayed()

def agent(mode, bidFn, playFn):
    game = Game(mode)
    game.play()

    bid = Bidding(bidFn)
    finalResult = bid.startBid()
    print("叫牌紀錄：", finalResult)
    print("===== 叫牌結束 ===================")
    play = Playing()

    play.contract = play.getContract()
    print("北家",deckValToStr(play.getDeck("northDeck")))
    print("牌桌",deckValToStr(play.getTableCards()))
    print("南家",deckValToStr(play.getDeck("southDeck")))
    print("叫牌結果：", play.getContract())
    print("莊家：", play.getDealer())
    print("分數：", play.getScore())
    print("王牌：",mapping.numToSuit[play.kingSuit()])
    play.dealer = mapping.teamNameToNum[play.getDealer()]
    sleep(1)
    while isMoving(play.getDeckNodes("northDeck")[0]):
        continue
    print("playing")
    now = play.dealer
    play.leader = (play.dealer+1)%4
    print(play.isEnd())
    while not play.isEnd():
        while True:
            cards = play.getTableCards()
            # print("table", deckValToStr(cards))
            now = play.playerNow()
            # print("playerNow", now)
            if now%2 and len(cards)<=4:
                break
            sleep(0.5)
        northDeck = play.getDeck("northDeck")
        southDeck = play.getDeck("southDeck")
        info = {
            'turn': "southDeck" if now==3 else "northDeck",
            'northDeck': list(map(mapping.deck.get, northDeck)),
            'southDeck': list(map(mapping.deck.get, southDeck)),
            'table': list(map(mapping.deck.get, play.getTableCards())),
            'king': play.king
        }
        pick = playFn(info)
        idx = info[info['turn']].index(pick)
        print(info['turn'], "click",mapping.valToCard[pick])
        play.waitForClick(info, idx)
        while True:
            sleep(0.5)
            cards = play.getTableCards()
            # print("table#", deckValToStr(cards))
            # print("playerNow#", play.playerNow(cards))
            if len(cards)!=4:
                if (play.playerNow(cards))%2 or\
                play.isEnd():
                    break
                continue
            print("回合結束：", deckValToStr(cards))
            nextPlayer = -1
            cardCmp = cards = list(map(mapping.deck.get, cards))
            firstSuit = int(cardCmp[0]/13)
            if play.king<4:
                cardCmp = list(map(lambda x: 1000+x if int(x/13)==play.king else 
                ( 100+x if int(x/13)==firstSuit else x)
                , cardCmp))
            else:
                cardCmp = list(map(lambda x: 100+x if int(x/13)==firstSuit else x, cardCmp))
            idx = cardCmp.index(max(cardCmp))
            print("最大：", mapping.valToCard[cards[idx]], cardCmp)
            play.leader=(play.leader+idx)%4
            if play.leader%2==0:
                while len(play.getTableCards())<4:
                    sleep(0.5)
            break
    print("end game")
    sleep(86400)
    driver.quit()