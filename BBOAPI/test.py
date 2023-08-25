bids = [
    "1C","1D","1H","1S","1nt",
    "2C","2D","2H","2S","2nt",
    "3C","3D","3H","3S","3nt",
    "4C","4D","4H","4S","4nt",
    "5C","5D","5H","5S","5nt",
    "6C","6D","6H","6S","6nt",
    "7C","7D","7H","7S","7nt",
    "Pass", "double", "redouble"
]
for i in range(len(bids)):
    print('"%s": %d,' % (bids[i], i))