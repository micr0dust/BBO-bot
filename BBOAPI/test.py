class a:
    def __init__(self):
        self.c=1
        self.b=self.c+1

    def pt(self):
        return self.b

an = a()
print(an.pt())