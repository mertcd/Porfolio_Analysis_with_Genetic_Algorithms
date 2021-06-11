import os
import matplotlib.pyplot as plt
import random


def makeDates(file):  # Just a function to save dates to an array. Necessary because we dont want to input holidays.
    dates = []
    for i in file:
        dates.append(i[:10])
    return dates


def makeList(file):  # After opening the file it adds all information to an array. We dont want to read all from disk
    lsi = []
    for line in file:
        lsi.append(line)
    return lsi


def stc_and_ma(stck, start, end):  # This function calculates "Moving Average" and "Stohastic Oscilator".
    sum = 0
    co = 0
    low = 99999
    high = 0
    inTime = False
    for line in stck:
        currentDay = line[:10]
        if currentDay == start:
            inTime = True
        # Here we search through daily stock records to find out correct time to calcuşate.
        if inTime:
            ls = line.split(",")
            sum += float(ls[1])
            co += 1
            if co > 15:#upper part saves 30 days prices and lover part calculates for stc
                lowPrice = float(ls[3])
                highPriceDaily = float(ls[2])
                if lowPrice < low: low = lowPrice
                if highPriceDaily > high: high = highPriceDaily
        if currentDay == end and co != 0 and high - low != 0:
            ls = line.split(",")
            closingPrice = float(ls[-3])
            # First element for calculatin stohastic oscilator other for calculating moving average.
            return [((closingPrice - low) / (high - low)) * 100, sum / co]
    return [0, 0]


def calculateGoldenCross(stock, seasonalMa, end, dates):
    weeklyMa = stc_and_ma(stock, dates[dates.index(end) - 7], end)[1]

    return weeklyMa - seasonalMa


def setParameters(stck, end, dates):
    stockArr = makeList(open("Stocks\\" + stck, "r"))
    stcWma = stc_and_ma(stockArr, dates[dates.index(end) - 30], end)
    ma = stcWma[1]
    stc = stcWma[0]
    goldenCross = calculateGoldenCross(stockArr, ma, end, dates)


    return [stck, goldenCross, stc]


def createPortfolio(stcks, length, end, dates):
    ls = []
    while len(ls) < length:
        randomStock = stcks[random.randint(0, len(stcks) - 1)]
        if randomStock not in ls:
            ls.append(setParameters(randomStock, end, dates))
    return ls


def createPopulation(stcks, portLength, length, end, dates):
    ls = []
    for i in range(length):
        ls.append(createPortfolio(stcks, portLength, end, dates))

    return ls


def calculateFitness(genome):
    maSum = 0
    stcSum = 0
    for gen in genome:
        maSum += gen[1]
        stcSum += gen[2]
    return  -maSum
    #- (stcSum+ maSum/ 10)
def crossOver(gen1 ,gen2):
    ch1 = gen1.copy()
    ch2 = gen2.copy()

    crossOverPoint = random.randint(0, 4)

    for i in range(crossOverPoint):
        temp = ch1[i]
        ch1[i] = ch2[i]
        ch2[i] = temp
    return [ch1, ch2]

def mutation(gen ,end, dates):
    por = gen.copy()

    mutationPoint = random.randint(0, 4)
    stcks = os.listdir("Stocks")
    randomStock = stcks[random.randint(0, len(stcks) - 1)]
    por[mutationPoint] =setParameters(randomStock, end, dates)
    return por
def sortPopulation(population):
    popu = population.copy()
    for i in range(len(popu)):


        min_idx = i
        for j in range(i + 1, len(popu)):
            if calculateFitness(popu[min_idx]) < calculateFitness(popu[j]):
                min_idx = j


        popu[i], popu[min_idx] = popu[min_idx], popu[i]
    return popu
def income(port,end,days):
    for i in port:
        stockArr = makeList(open("Stocks\\" + i[0], "r"))
        date = makeDates(stockArr)
        try:
            idx = date.index(end)
        except:
            return 0
        buyingPrice =stockArr[idx].split(",")[1]
        sellingPrice= stockArr[idx+days].split(",")[1]
        return float(buyingPrice)-float(sellingPrice)
if __name__ == '__main__':
    stc = open("Stocks\\abax.txt", "r")
    sta = makeList(stc)
    dateList = makeDates(sta)

    a = 0
    stocknames = os.listdir("Stocks")
    for i in range(10):
        popu = createPopulation(stocknames, 5, 20, "2017-03-24", dateList)

        co = 0


        while co < 200:
            co+=1
            popu = sortPopulation(popu)
            popu= popu[:20]
            for i in range(20):
                newBorn1 =crossOver(popu[-1],popu[-2])[0]

                a = random.randint(0,10)
                if a >5:
                    newBorn1 = mutation(newBorn1, "2017-03-24", dateList)
                popu.append(newBorn1)
        a+=income(popu[-1], "2017-03-24",20)


    print(a)

"""    for i in range(len(popu)):
        print("%f" % calculateFitness(popu[i]))
"""