import os

stock_names=open("aaaaastock_names","w")



files = os.listdir("C:\\Users\\Monster\\Desktop\\Porfolio Analysis with Genetic Algorithms")
print(files)


aple = open("aame.us.txt", "r")
times = open("aaaall_times.txt","w")
ls = []
for line in aple:
    ls.append(line[:10])

times.write(",".join(ls))