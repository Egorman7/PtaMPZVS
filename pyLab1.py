class Alpha:
    count = 0
    def __init__(self, value):
        self.value = value
        if Alpha.count==0:
            print("First element created! Value = ", self.value)
        Alpha.count+=1
    def __del__(self):
        Alpha.count-=1
        if Alpha.count==0:
            print("Last element deleted! Value = ", self.value)

def main():
    a1 = Alpha(1)
    a2 = Alpha(2)
    a3 = Alpha(3)
    a1 = 2
    a3 = 1
    a2 = 3


main()
