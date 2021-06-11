import os

files = os.listdir("C:\\Users\\Monster\\Desktop\\Porfolio Analysis with Genetic Algorithms\\Stocks")

for file in files:
    fi = open("C:\\Users\\Monster\\Desktop\\Porfolio Analysis with Genetic Algorithms\\Stocks\\"+file,"r")
    a = file
    b = a[:-6]
    c = b+"txt"
    print(b)
    wi = open("C:\\Users\\Monster\\Desktop\\Porfolio Analysis with Genetic Algorithms\\aaaabc\\"+c,"w")
    co =0
    for line in fi:

        if co!=0 and int(line[:4])>2015 :
            wi.write(line)

        co+=1