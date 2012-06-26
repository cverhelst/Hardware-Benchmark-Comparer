import urllib2
import sys
import re
from BeautifulSoup import BeautifulSoup

class Parser(object):

    @staticmethod
    def parse(url=None):
        if url is not None:
            page = urllib2.urlopen(url)
        else:
            print "Printing example:"
            page = open("test.html");
        soup = BeautifulSoup(page)

        blueName = soup.find("div",{ 'class' : "vs_box left" }).div.text
        blackName = soup.find("div", { 'class' : "vs_box right"}).div.text

        benches  = soup.findAll(id=re.compile('^product_'))

        names = []

        ratios = [];
        blueWins = 0;
        blackWins = 0;

        for bench in benches:

            b = bench.find("div", { 'class' : "bench_title"})
        
            try:
                name = b.span.text
            except:
                name = b.a.text
            higher = "Lower" not in bench.find("div", { 'class' : "bench_title"}).text

            blueScore = round(float(bench.find("div",{ 'class' : "poll_blue" }).div.text),1)
            blackScore = round(float(bench.find("div",{ 'class' : "poll_black" }).div.text),1)

            blueIsBetter = blueScore > blackScore if higher else blueScore < blackScore
            if blueIsBetter:
                blueWins += 1                    
            else:
                blackWins += 1
            
            if higher:
                ratio = blueScore / blackScore   
            else:
                ratio = blackScore / blueScore

            ratios.append(ratio)

            higher = "Higher" if higher else "Lower"

            names.append([name,higher,blueScore,blackScore])

        maxLength = 60
        first = int(maxLength - maxLength * 0.4)
        last = maxLength - first - 3
        justify = 9


        print "\tBlue  \t%s" % blueName
        print "\tBlack \t%s" % blackName

        print "\n%s   %s | %s | %s\n" % ("Bench".center(maxLength),
                                        "Best".center(justify),
                                        "Blue".center(justify),
                                        "Black".center(justify))

        
        for name in names:

            bench = name[0]

            if len(bench) > maxLength:
                bench = bench[:first] + "..." + bench[-last:]

            print "%s - %s | %s | %s" % (bench.ljust(maxLength),
                                        name[1].center(justify),
                                        str(name[2]).rjust(justify),
                                        str(name[3]).rjust(justify))
        msg = "Wins out of %d total benches" % len(ratios)
        print "\n%s   %s   %s | %s\n" % (msg.center(maxLength),
                                        "".center(justify),
                                        str(blueWins).center(justify),
                                        str(blackWins).center(justify))

        ratioSum = 0

        for ratio in ratios:
            ratioSum += ratio

        ratio = ratioSum / len(ratios)
        if ratio >= 1:
            
            bestRatio = (ratio * 100) - 100
            worstRatio = 100 - (1/ratio * 100)
            best = "Blue"
            worst = "Black"
        else:
            worstRatio = 100 - (ratio * 100)
            bestRatio = (1/ratio * 100) - 100
            best = "Black"
            worst = "Blue"
            
        bestPerformance = (best,bestRatio,"better",worst)
        worstPerformance = (worst,worstRatio,"worse",best)

        print "\n%s is %.2f %s %s than %s" % (bestPerformance[0],bestPerformance[1],"%",bestPerformance[2],bestPerformance[3])

        print "\n%s is %.2f %s %s than %s" % (worstPerformance[0],worstPerformance[1], "%",worstPerformance[2],worstPerformance[3])

        price = raw_input("Compare prices? ")

        if price.lower() in ("y","yes","yeah","sure","yes please","yes, please"):

            bluePrice = float(raw_input("Please enter the price of Blue: "))
            blackPrice = float(raw_input("Please enter the price of Black: "))

            priceRatio = blackPrice / bluePrice
            if priceRatio >= 1:
                bestRatio = 100 - (1/priceRatio * 100)
                worstRatio = (priceRatio * 100) - 100
                best = "Blue"
                worst = "Black"
                    
            else:
                bestRatio = 100 - (priceRatio * 100)
                worstRatio = (1/priceRatio * 100) - 100
                best = "Black"
                worst = "Blue"

            bestPrice = (best,bestRatio,"cheaper",worst)
            worstPrice = (worst,worstRatio,"more expensive",best)

            print "\n%s is %.2f %s %s than %s" % (bestPrice[0],bestPrice[1],"%", bestPrice[2], bestPrice[3])
            if bestPerformance[0] == bestPrice[0]:
                print "while being %.2f %s %s than %s" % (bestPerformance[1],bestPerformance[2],"%",bestPerformance[3])
            else:
                print "while being %.2f %s %s than %s" % (worstPerformance[1],worstPerformance[2],"%",worstPerformance[3])

            print "\n%s is %.2f %s %s than %s" % (worstPrice[0],worstPrice[1], "%", worstPrice[2],worstPrice[3])
            if worstPerformance[0] == worstPrice[0]:
                print "while being %.2f %s %s than %s" % (worstPerformance[1],worstPerformance[2],"%",worstPerformance[3])
            else:
                print "while being %.2f %s %s than %s" % (bestPerformance[1],bestPerformance[2],"%",bestPerformance[3])
            

if __name__ == '__main__':

    if(len(sys.argv) > 1):
        Parser.parse(sys.argv[1])
    else:
        Parser.parse()

    
