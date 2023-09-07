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

debug = False

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
    return attrs

def getAllCards():
    cards = driver.execute_script("return document.querySelectorAll('.gwt-Image')")
    # cards = driver.find_elements(By.CSS_SELECTOR, ".gwt-Image")
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
def plotCard(cards):
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

def waitFor(fn, interval):
    sleep(0.5)
    while not fn():
        sleep(0.5)

class Game:
    def __init__(self, mode):
        self.mode = mode

    def notHereBtnChecker(self):
        popup = driver.execute_script('return document.querySelector(".contentPane")')
        if popup:
            driver.execute_script('document.querySelector(".contentPane").getElementsByTagName("button")[0].click()')

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
    def __init__(self, beforeBidFn, bidFn, bidEndFn, rounds):
        self.beforeBidFn = beforeBidFn
        self.bidFn = bidFn
        self.bidEndFn = bidEndFn
        self.rounds = rounds

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
        return cards
        
    def startBid(self):
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".biddingBoxPassButton")))
        southDeck = list(map(mapping.deck.get ,self.getDeck()))
        self.beforeBidFn(southDeck)
        maxBid = -1
        bidding = True
        while(bidding):
            if not bidding:
                break
            bidLst = self.getBid()
            maxBid = self.maxBidVal(bidLst) if len(bidLst) else -1
            bid = self.bidFn({
                'rounds': self.rounds,
                'mydeck': southDeck,
                'maxBid': maxBid,
                'bidLst': bidLst
            })
            self.bidAction(mapping.idToAction[bid])
            try:
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".biddingBoxPassButton")))
            except:
                bidding = False
        final = self.getBid()
        self.bidEndFn(final)
        return final


class Playing:
    def __init__(self, beforePlayFn, playFn, roundEndFn):
        self.beforePlayFn = beforePlayFn
        self.playFn = playFn
        self.roundEndFn = roundEndFn
        self.dealer = -1
        self.leader = -1
        self.contract = -1
        self.trump = -1
        self.rounds = 0

    def getDeck(self, name):
        # northDeck, southDeck
        while True:
            try:
                cards = driver.execute_script('return document.getElementById("'+name+'").getElementsByTagName("img")')
                return cardsFromNodes(cards) if cards else []
            except:
                sleep(0.1)
    
    def getDeckNodes(self, name):
        # northDeck, southDeck
        return driver.execute_script('return document.getElementById("'+name+'").getElementsByTagName("img")')
        # return driver.find_element(By.ID, name).find_elements(By.TAG_NAME, "img")
    
    def getTableCards(self):
        while True:
            try:
                return cardsFromNodes(getAllCards()[
                    len(self.getDeck("southDeck"))+len(self.getDeck(self.getAnotherDeck())):
                ])
            except:
                sleep(0.1)
    # 最終叫牌結果(合約)
    def getContract(self):
        return driver.find_element(By.ID, "contract").text
    # 莊家
    def getDealer(self):
        return driver.find_element(By.ID, "dealer").text
    # 分數
    def getScore(self):
        return int(driver.find_element(By.ID, "score").text)

    def trumpSuit(self):
        if "♣" in self.contract:
            return 0
        elif "♦" in self.contract:
            return 1
        elif "♥" in self.contract:
            return 2
        elif "♠" in self.contract:
            return 3
        elif "NT" in self.contract:
            return 4
        return self.trump

    def playerNow(self, table=None):
        if table != None:
            return (self.leader+len(table))%4
        return (self.leader+len(self.getTableCards()))%4

    def waitForClickByIdx(self, info, idx):
        originLen = len(self.getDeckNodes(info['turn']))
        while len(self.getDeckNodes(info['turn'])) == originLen:
            realClick(self.getDeckNodes(info['turn'])[idx])
            sleep(0.5)

    def isEnd(self):
        endBtn = driver.execute_script('return document.querySelector(".dealEndPanel")')
        return endBtn.is_displayed()

    def isMyturn(self):
        cards = self.getTableCards()
        if len(cards)>4:
            return False
        if self.dealer%2:
            return self.playerNow()%2
        return self.playerNow()==3

    def waitForMyTurn(self):
        while True:
            cards = self.getTableCards()
            if self.isEnd():
                break
            if self.isMyturn() and len(cards)<=4:
                break
            sleep(0.5)
        return self.playerNow()

    def playInit(self):
        driver.execute_script("\
            let bidRes = document.querySelector('.widgetPanel').querySelector('.contractPanel');\
            bidRes.querySelector('.gwt-HTML').id = 'contract';\
            bidRes.querySelector('.gwt-Label').id = 'dealer';\
            document.querySelector('.scorePanelTop').nextSibling.id = 'score';\
        ")
        self.dealer = mapping.teamNameToNum[self.getDealer()]
        self.contract = self.getContract()
        self.trump = self.trumpSuit()
        self.leader = (self.dealer+1)%4

    def getAnotherDeck(self):
        if self.dealer%2:
            return "northDeck"
        if self.dealer==0:
            return "eastDeck"
        if self.dealer==2:
            return "westDeck"

    def posElementsInit(self):
        if self.dealer%2:
            cardsEle = driver.find_elements(By.CSS_SELECTOR, ".gwt-Image")
            driver.execute_script("arguments[0].id='southDeck'", cardsEle[0].find_element("xpath", ".."))
            driver.execute_script("arguments[0].id='northDeck'", cardsEle[13].find_element("xpath", ".."))
            while not len(self.getDeckNodes("northDeck")):
                sleep(0.5)
            waitFor(lambda: not isMoving(self.getDeckNodes("northDeck")[0]),0.5)
        elif self.dealer==0:
            cardsEle = driver.find_elements(By.CSS_SELECTOR, ".gwt-Image")
            driver.execute_script("arguments[0].id='eastDeck'", cardsEle[0].find_element("xpath", ".."))
            driver.execute_script("arguments[0].id='southDeck'", cardsEle[13].find_element("xpath", ".."))
            while not len(self.getDeckNodes("eastDeck")):
                sleep(0.5)
            waitFor(lambda:not isMoving(self.getDeckNodes("eastDeck")[0]),0.5)
        elif self.dealer==2:
            cardsEle = driver.find_elements(By.CSS_SELECTOR, ".gwt-Image")
            driver.execute_script("arguments[0].id='southDeck'", cardsEle[0].find_element("xpath", ".."))
            self.firstCard()

    def roundEndChecker(self):
        sleep(0.2)
        cards = self.getTableCards()
        if len(cards)!=4:
            if self.isMyturn() or\
            self.isEnd():
                return True
            return False
        self.rounds+=1
        nextPlayer = -1
        cardCmp = cards = list(map(mapping.deck.get, cards))
        firstSuit = int(cardCmp[0]/13)
        if self.trump<4:
            cardCmp = list(map(lambda x: 1000+x if int(x/13)==self.trump else 
            ( 100+x if int(x/13)==firstSuit else x)
            , cardCmp))
        else:
            cardCmp = list(map(lambda x: 100+x if int(x/13)==firstSuit else x, cardCmp))
        idx = cardCmp.index(max(cardCmp))
        self.roundEndFn({
            'table': cards,
            'maxIdx': idx
        })
        self.leader=(self.leader+idx)%4
        if not self.isMyturn():
            waitFor(lambda:len(self.getTableCards())<4 or self.isEnd(), 0.5)
        return True

    def firstCard(self):
        southDeck = self.getDeck("southDeck")
        info = {
            'turn': "southDeck",
            'southDeck': list(map(mapping.deck.get, southDeck)),
            'table': [],
            'trump': self.trump,
            'dreamer': (self.dealer+2)%4
        }
        pick = self.playFn(info)
        idx = info[info['turn']].index(pick)
        self.waitForClickByIdx(info, idx)
        waitFor(lambda:len(getAllCards())>20, 0.5)
        cardsEle = driver.find_elements(By.CSS_SELECTOR, ".gwt-Image")
        driver.execute_script("arguments[0].id='westDeck'", cardsEle[0].find_element("xpath", ".."))
        waitFor(self.roundEndChecker, 0.5)

    def endBtnClick(self):
        while True:
            try:
                btn = driver.execute_script('return document.querySelector(".dealEndPanel")')
                realClick(btn)
                return
            except:
                sleep(0.5)

    def nextPlay(self):
        while True:
            now = self.waitForMyTurn()
            if self.isEnd():
                return
            another = self.getDeck(self.getAnotherDeck())
            southDeck = self.getDeck("southDeck")
            info = {
                'turn': "southDeck" if not self.dealer%2 or now==3 else self.getAnotherDeck(),
                self.getAnotherDeck(): list(map(mapping.deck.get, another)),
                'southDeck': list(map(mapping.deck.get, southDeck)),
                'table': list(map(mapping.deck.get, self.getTableCards())),
                'trump': self.trump
            }
            if not len(info[info['turn']]) or len(getAllCards())>50:
                continue
            pick = self.playFn(info)
            idx = info[info['turn']].index(pick)
            self.waitForClickByIdx(info, idx)
            waitFor(self.roundEndChecker, 0.5)
            return

    def startPlay(self):
        sleep(1)
        try:
            self.playInit()
        except:
            if self.isEnd():
                self.beforePlayFn({
                    'contract': "Pass",
                    'trump': None,
                    'dealer': None,
                    'score': None
                })
                return True
            return False
        waitFor(lambda: driver.find_element(By.ID, "dealer").is_displayed(), 0.5)
        self.beforePlayFn({
            'contract': self.contract,
            'trump': self.trump,
            'dealer': self.dealer,
            'score': self.getScore(),
            'dreamer': (self.dealer+2)%4
        })
        self.posElementsInit()
        waitFor(lambda: not isMoving(self.getDeckNodes(self.getAnotherDeck())[0]), 0.5)
        while not self.isEnd():
            self.nextPlay()
        return self.isEnd()


def agent(mode, maxRounds, beforeBidFn, bidFn, bidEndFn, beforePlayFn, playFn, roundEndFn, gameEnd):
    game = Game(mode)
    game.play()
    rounds = 0
    while rounds<maxRounds:
        rounds+=1
        bid = Bidding(beforeBidFn, bidFn, bidEndFn, rounds)
        play = Playing(beforePlayFn, playFn, roundEndFn)
        finalResult = bid.startBid()
        if not play.startPlay():
            break
        play.endBtnClick()
        gameEnd({
            'round': rounds,
            'score': play.getScore()
        })
        game.notHereBtnChecker()
    driver.quit()