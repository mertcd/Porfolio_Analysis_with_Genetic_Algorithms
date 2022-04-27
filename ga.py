import os
import matplotlib.pyplot as plt
import random

# Just a function to save dates to an array. Necessary because we dont want to input holidays.
def makeDates(file):  
    dates = []
    for i in file:
        dates.append(i[:10])
    return dates

 # After opening the file it adds all information to an array. We dont want to read all from disk
def makeList(file): 
    lsi = []
    for line in file:
        lsi.append(line)
    return lsi

# This function calculates "Moving Average" and "Stohastic Oscilator".
def stc_and_ma(stck, start, end):  
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
            #upper part saves 30 days prices and lover part calculates for stc
            if co > 15:
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
    #If short term moving average cross the long term moving average golden cross occurs
    return weeklyMa - seasonalMa 

# Function for adding paramaterss to genome  So we dont need traverse all the
def setParameters(stck, end, dates):
    # list on fitness calculation
    stockArr = makeList(open("Stocks\\" + stck, "r"))
    stcWma = stc_and_ma(stockArr, dates[dates.index(end) - 30], end)
    ma = stcWma[1]
    stc = stcWma[0]
    closingPrice = stockArr[dateList.index("2017-03-24")].split(",")[1]
    monthBeforePrice= stockArr[dateList.index("2017-03-24")-24].split(",")[1]
    goldenCross = calculateGoldenCross(stockArr, ma, end, dates)


    return [stck, goldenCross, stc,float(closingPrice)-float(monthBeforePrice)]

# Creates the portfolio to be encoded as a genome or invidual in population
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

    return ls #Create the population of genomes.

#Calculates fitness based on parameter that encoded into gene.
def calculateFitness(genome):
    maSum = 0
    stcSum = 0
    momentum = 0
    for gen in genome:
        maSum += gen[1]
        stcSum += gen[2]
        momentum+=gen[3]
    return  (stcSum/200+ maSum/ 5-momentum*10)*-1
#Single point cross over.
def crossOver(gen1 ,gen2):
    ch1 = gen1.copy()
    ch2 = gen2.copy()

    crossOverPoint = random.randint(0, 4)

    for i in range(crossOverPoint):
        temp = ch1[i]
        ch1[i] = ch2[i]
        ch2[i] = temp
    return [ch1, ch2]
#Mutations are importent for not to be premature.
def mutation(gen ,end, dates):
    por = gen.copy()

    mutationPoint = random.randint(0, 4)
    stcks = os.listdir("Stocks")
    randomStock = stcks[random.randint(0, len(stcks) - 1)]
    por[mutationPoint] =setParameters(randomStock, end, dates)
    return por
#Sorts the population using selection sort.
def sortPopulation(population): 
    popu = population.copy()
    for i in range(len(popu)):


        min_idx = i
        for j in range(i + 1, len(popu)):
            if calculateFitness(popu[min_idx]) < calculateFitness(popu[j]):
                min_idx = j


        popu[i], popu[min_idx] = popu[min_idx], popu[i]
    return popu
#Calculates income to test the fitness values .
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
    file =open("income.txt","w")
    c = 0
    stocknames = os.listdir("Stocks")


    #creates population of portfolios encoded as genome.
    popu = createPopulation(stocknames, 5,20, "2017-04-24", dateList)

    co = 0

    fitnessValues = []
    proValues = []
    while co < 30: #Make 30 iteration
        co+=1
        popu = sortPopulation(popu)
        #20 best ones to survive next generation
        popu= popu[:20]
        fitnessValues.append(calculateFitness(popu[0]))
        for i in range(20):#create 20 new individual
            newBorn1 =crossOver(popu[-1],popu[-2])[0]

            a = random.randint(0,10)
            if a >0:
                newBorn1 = mutation(newBorn1, "2017-04-24", dateList)
                popu.append(newBorn1)
        profit = income(popu[0], "2017-04-24", 20)
        proValues.append(profit)



    print(fitnessValues)
    steps = [i for i in range(len(fitnessValues))]
    plt.plot(steps,fitnessValues)
    plt.show()
    plt.plot(steps,proValues)
    plt.show()
"""    for i in range(len(popu)):
        print("%f" % calculateFitness(popu[i]))
"""
