import base64
import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from mapping import deck

cards = list(deck.keys())

def printCard(cards):
    fig = plt.figure()
    for i in range(len(cards)):
        img = mpimg.imread(io.BytesIO(base64.b64decode(cards[i])), format='PNG')
        fig.add_subplot(4, 13, i+1)
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(img)
    plt.show()

printCard(cards)