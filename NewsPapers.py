import feedparser as fp
import json
import newspaper
from newspaper import Article
import time
from time import mktime, sleep
from datetime import datetime
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import textwrap3
import sys
from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime, date
import requests
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

print("Nomeon News Digest [Version 5.1] ")
print("(c) 2018 Wakili.AI. All rights reserved. ")
print("\n")
print("***NEWS DIGEST***. ")

def main():
    print("\n")
    print("Pick a category")
    print("1. News Digest\n2. Nairobi Stock Exchange")
    print("\n")
    mat=input("Answer: ")
    req = Request("https://www.google.com/ ")
    try:
        response = urlopen(req)
    except URLError as e:
        print("No Connection :( ")
        print("Please check your internet connection and try again. Closing in 5 seconds.")
        time.sleep(6)
        sys.exit()
        time.sleep(0.5)

    if mat=="1":
        # Set the limit for number of articles to download
        LIMIT = 4
        data = {}
        data['newspapers'] = {}
        print("* Please be patient as Nomeon collects the news. ")
        print("* Nomeon will predict whether an article is fake news or not.")
        time.sleep(1)
        
        # Loads the JSON files with news sites
        with open('News.json') as data_file:
            companies = json.load(data_file)

        # Iterate through each news company
        for company, value in companies.items():    
            if 'rss' in value:
                d = fp.parse(value['rss'])
                print("Downloading articles from ", company)
                newsPaper = {
                    "rss": value['rss'],
                    "link": value['link'],
                    "articles": []
                }
                for entry in d.entries:
                    if hasattr(entry, 'published'):
                        if count > LIMIT:
                            break
                        article = {}
                        article['link'] = entry.link
                        date = entry.published_parsed
                        article['published'] = datetime.fromtimestamp(mktime(date)).isoformat()
                        try:
                            content = Article(entry.link)
                            content.download()
                            content.parse()
                        except Exception as e:
                            print(e)
                            print("continuing...")
                            continue
                        article['title'] = content.title
                        article['text'] = content.text
                        newsPaper['articles'].append(article)
                        print("Article", count, "downloaded from", company, ", url: ", entry.link)
                        count = count + 1
            else:
                with open('News.json') as data_file:
                    companies = json.load(data_file)
                print("\n")
                print("Fetching ", company, "......")
                count = 1
                print("\n")
                paper = newspaper.build(value['link'], memoize_articles=False)
                newsPaper = {
                    "link": value['link'],
                    "articles": []
                }
                noneTypeCount = 0
                
                for content in paper.articles:
                    if count > LIMIT:
                        break
                    try:
                        content.download()
                        content.parse()
                        content.nlp()
                    except Exception as e:
                        print(e)
                        print("continuing...")
                        continue
                    
                    article = {}
                    article['title'] = content.title
                    article['text'] = content.text
                    article['link'] = content.url
                    article['summary']=content.summary
                    newsPaper['articles'].append(article)
                    
                    blob=TextBlob(content.text)
                    subjectivity= blob.sentiment.subjectivity
                    blob= TextBlob(content.text, analyzer = NaiveBayesAnalyzer())
                    positive= blob.sentiment.p_pos
                    negative= blob.sentiment.p_neg
                        
                    print(count, ")", content.title)
                    print("\n")
                    list=textwrap3.wrap(content.summary, width=95)
                    for element in list:
                        print(element)
                    print("\n")
                    print("Link")
                    print(content.url)
                    print("\n")
                    subjective= round(subjectivity)
                    mild_bias=0.5 or 0.6 or 0.7
                    extreme_bias=0.8 or 0.9 or 1
                    objective= 0 or 0.1 or 0.2 or 0.3 or 0.4
                    if subjective>=mild_bias:
                        print("***Reliability***")
                        print("Read with caution. Confirm factual information. ")
                    elif subjective<=objective:
                        print("***Reliability***")
                        print("This story is reliable.")
                    elif subjective<mild_bias:
                        print("***Reliability***")
                        print("Read with caution. Confirm factual information.")
                    elif objective>=subjective:
                        print("***Reliability***")
                        print("This story is reliable. ")
                    elif subjective>=extreme_bias:
                        print("***Reliability***")
                        print("Read with extreme caution. Misinformation traces detected.")
                        
                    print("********************")
                    print("\n")
                    count = count + 1
                    noneTypeCount = 0
                    data['newspapers'][company] = newsPaper
                    import csv                    
                    with open('NewsDigest.csv', 'a', encoding='utf-8') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow(['Company', "Title", 'Text', 'Link', "Reliability"])
                        Company=company
                        Title= article['title']
                        Text= article['text']
                        Link= article['link']
                        Reliability=round(subjectivity)
                        writer.writerow([Company, Title, Text, Link, Reliability])

        print("The News have been collated and saved in file called 'NewsDigest' for your further analysis. ")

    if mat=="2":
        URL1= 'https://live.mystocks.co.ke/'
        URL2 = 'https://live.mystocks.co.ke/price_list/'
        payload = {
                        "Username": "mwago.gatahi@gmail.com",
                        "Password": "9whZZKFP"
                    }
        with requests.Session() as session:
            post = session.post(URL1, data=payload)
            r = session.get(URL2)

        print("\n")
        print("********************")
        print("Nairobi Stock Exchange (NSE) Data Aggregator. ")
        print(datetime.now())
        print("********************")
        print("\n")
        print("Pick a category. ")
        print("1. Industries ")
        print("2. Indices")
        choice=input("Your choice? ")
        print("\n")
    
    
        if choice =="1":
            print("Pick an industry. ")
            print("\n")
            print("1. Agricultural\n2. Automobiles\n3. Banking\n4. Commercial Services\n5. Construction & Allied\n6. Energy\n7. Insurance\n8. Investment\n9. Investment Services\n10. Manufacturing and Allied\n11. Telecoms\n")
            print("\n")
            jibu=input("Answer: ")
            
            if jibu=="1":
                print("\n")
                print("Agriculture")
                print("Companies include 1 coffee company, 4 Tea companies and 1 multi-agricultural company. ")
                print("Generating data.....")
                print("\n")
                name="***Eaagads (EGAD)***"
                name1="Eaagads"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=EGAD"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("Eaagads.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")
                
                print("\n")
                name="***Kakuzi (KUKZ)***"
                name1="Kakuzi Tea"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=KUKZ"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("Kakuzi Tea.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")
                
                print("\n")
                name="***Kapchorua Tea Kenya Plc (KAPC)***"
                name1="Kapchorua Tea"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=KAPC"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)

                import csv
                with open("KapchoruaTea.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("\n")
                print("********************")

                print("\n")
                name="***Limuru Tea Kenya Plc (LIMT)***"
                name1="Limuru Tea"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=LIMT"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)

                import csv
                with open("Limuru Tea.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("\n")
                print("********************")

                print("\n")
                name="***Sasini Tea Kenya Plc (SASN)***"
                name1="Sasini Tea"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=SASN"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("Sasini Tea.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("\n")
                print("********************")

                print("\n")
                name="***Williamson Tea Kenya Plc (WTK)***"
                name1="Williamson Tea"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=WTK"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("Williamson Tea.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("\n")
                print("********************")

                import shutil
                import glob
                path = r'C:\Users\USER\Desktop\Day to day AI\Nomeon\Media\Financial Data\Industries\NSE'
                allFiles = glob.glob(path + "/*.csv")
                with open('Agriculture.csv', 'wb') as outfile:
                    for i, fname in enumerate(allFiles):
                        with open(fname, 'rb') as infile:
                            if i != 0:
                                infile.readline()  # Throw away header on all but first file
                                # Block copy rest of file from input to output without parsing
                            shutil.copyfileobj(infile, outfile)
                            print(fname + " has been imported.")
                            print("\n")
                
            if jibu=="2":
                print("Automobiles")
                print("Car and General is the only listed company in automobiles. ")
                print("Generating data.....")
                print("\n")
                name="***Car & General (C&G)***"
                name1="Car & General"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=C%2526G"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("CarGeneral.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")
                
                import shutil
                import glob
                path = r'C:\Users\USER\Desktop\Day to day AI\Nomeon\Media\Financial Data\Industries\NSE'
                allFiles = glob.glob(path + "/*.csv")
                with open('AutoMobiles.csv', 'wb') as outfile:
                    for i, fname in enumerate(allFiles):
                        with open(fname, 'rb') as infile:
                            if i != 0:
                                infile.readline()  # Throw away header on all but first file
                                # Block copy rest of file from input to output without parsing
                            shutil.copyfileobj(infile, outfile)
                            print(fname + " has been imported.")
                            print("\n")

            if jibu=="3":
                print("Bank")
                print("11 out of 43 licensed banks are listed on the NSE. ")
                print("Generating data.....")
                print("\n")
                name="***Barclays Bank (BBK)***"
                name1="Barclays Bank"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=BBK"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                #open a csv file with append, so old data will not be erased
                with open("Barclays.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Co-operative Bank of Kenya Ltd (COOP)***"
                name1="Co-operative Bank"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=COOP"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                #open a csv file with append, so old data will not be erased
                with open("Co-op.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Diamond Trust Bank Kenya Ltd (DTK)***"
                name1="Diamond Trust Bank"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=DTK"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                #open a csv file with append, so old data will not be erased
                with open("DiamondTrustBank.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Equity Group Holdings Ltd (EQTY)***"
                name1="Equity Bank"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=EQTY"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("Equity-Bank.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***HF Group Limited (HFCK)***"
                name1="Housing Finance"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=HFCK"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("HousingFinance.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***I&M Bank***"
                name1="I&M Bank"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=I%2526M"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("I&M.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***KCB Bank***"
                name1="KCB Bank"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=KCB"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("KCB.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***National Bank of Kenya***"
                name1="National Bank"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=NBK"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("NationalBank.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***NIC Bank Kenya***"
                name1="NIC Bank"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=NIC"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("NIC Bank.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Stanbic Holdings Plc***"
                name1="Stanbic Holdings Bank"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=CFC"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("StanbicHoldings.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Standard Chartered Bank Kenya Ltd (SCBK)***"
                name1="Standard Chartered"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=CFC"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("StanChart Bank.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")
                import shutil
                import glob
                path = r'C:\Users\USER\Desktop\Day to day AI\Nomeon\Media\Financial Data\Industries\NSE'
                allFiles = glob.glob(path + "/*.csv")
                with open('Banking.csv', 'wb') as outfile:
                    for i, fname in enumerate(allFiles):
                        with open(fname, 'rb') as infile:
                            if i != 0:
                                infile.readline()  # Throw away header on all but first file
                                # Block copy rest of file from input to output without parsing
                            shutil.copyfileobj(infile, outfile)
                            print(fname + " has been imported.")
                            print("\n")

                            
            if jibu=="4":
                print("Public companies in Commerce and Services include those in Media, publishing, aviation, retail, fashion and hospitality. ")
                print("Generating data.....")
                print("\n")
                name="***Deacons (East Africa) PLC (DCON)***"
                name1="Deacons"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=DCON"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("Deacons.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Eveready East Africa Ltd (EVRD)***"
                name1="Eveready"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=EVRD"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("Eveready.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Express Ltd (XPRS)***"
                name1="Express"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=XPRS"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("Express.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Kenya Airways Ltd (KQ)***"
                name1="KQ"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=KQ"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("KQ.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Longhorn Kenya Ltd (LKL)***"
                name1="LongHorn"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=LKL"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("Longhorn.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Nairobi Business Ventures***"
                name1="Nairobi Business Ventures"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=NBV"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("NairobiBusiness.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Nation Media Group Plc (NMG)***"
                name1="Nation Media"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=NMG"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("NationMedia.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Sameer Africa Ltd (FIRE)***"
                name1="Sameer"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=FIRE"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("Sameer.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")
                
                print("\n")
                name="***Standard Group Ltd (SGL)***"
                name1="Standard Group"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=SGL"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("Standard.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***TPS Eastern Africa (Serena) Ltd (TPSE)***"
                name1="TPS Serena"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=TPSE"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("TPSSerena.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Uchumi Supermarket Ltd (UCHM)***"
                name1="Uchumi"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=UCHM"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("Uchumi.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***WPP ScanGroup PLC (SCAN)***"
                name1="ScanGroup"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=SCAN"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                import csv
                #open a csv file with append, so old data will not be erased
                with open("ScanGroup.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")
                
                import shutil
                import glob
                path = r'C:\Users\USER\Desktop\Day to day AI\Nomeon\Media\Financial Data\Industries\NSE'
                allFiles = glob.glob(path + "/*.csv")
                with open('Commercial&Services.csv', 'wb') as outfile:
                    for i, fname in enumerate(allFiles):
                        with open(fname, 'rb') as infile:
                            if i != 0:
                                infile.readline()  # Throw away header on all but first file
                                # Block copy rest of file from input to output without parsing
                            shutil.copyfileobj(infile, outfile)
                            print(fname + " has been imported.")
                            print("\n")
         
            if jibu=="5":
                
                print("\n")
                print("Publicly Listed Companies in Construction include 3 cement companies, 1 cable installation company and 1 paint manufacturer. ")
                print("Generating data.....")
                print("\n")
                name="***ARM Cement Ltd (ARM)***"
                name1="ARM Cement"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=ARM"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                 
                import csv
                with open("ARMCement.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Bamburi Cement Ltd (BAMB)***"
                name1="Bamburi Cement"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=BAMB"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("BamburiCement.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Crown Berger Ltd (BERG)***"
                name1="Crown Berger"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=BERG"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("CrownBerger.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***East African Cables Ltd (CABL)***"
                name1="EACables"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=CABL"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("EACables.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***East African Portland Cement Ltd (PORT)***"
                name1="PortlandCement"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=PORT"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("PortlandCement.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")
                import shutil
                import glob
                path = r'C:\Users\USER\Desktop\Day to day AI\Nomeon\Media\Financial Data\Industries\NSE'
                allFiles = glob.glob(path + "/*.csv")
                with open('Construction.csv', 'wb') as outfile:
                    for i, fname in enumerate(allFiles):
                        with open(fname, 'rb') as infile:
                            if i != 0:
                                infile.readline()  # Throw away header on all but first file
                                # Block copy rest of file from input to output without parsing
                            shutil.copyfileobj(infile, outfile)
                            print(fname + " has been imported.")
                            print("\n")
            

            if jibu=="11":
                print("\n")
                print("Safaricom is the only listed company in technology and telecommunications ")
                print("Generating data.....")
                print("\n")
                name="***Safaricom Plc (SCOM)***"
                name1="Safaricom"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=SCOM"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("Safaricom.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")
                import shutil
                import glob
                path = r'C:\Users\USER\Desktop\Day to day AI\Nomeon\Media\Financial Data\Industries\NSE'
                allFiles = glob.glob(path + "/*.csv")
                with open('Technology.csv', 'wb') as outfile:
                    for i, fname in enumerate(allFiles):
                        with open(fname, 'rb') as infile:
                            if i != 0:
                                infile.readline()  # Throw away header on all but first file
                                # Block copy rest of file from input to output without parsing
                            shutil.copyfileobj(infile, outfile)
                            print(fname + " has been imported.")
                            print("\n")

            if jibu=="6":
                print("\n")
                print("In the energy sector, we have 2 petroluem companies, 2 Kenyan electricity distributors and 1 Ugandan Electricity Distributor. ")
                print("Generating data.....")
                print("\n")
                name="***KenolKobil Ltd (KENO)***"
                name1="KenolKobil"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=KENO"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("KenolKobil.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Kenya Electricity Generating Company Ltd (KEGN)***"
                name1="KenGen"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=KEGN"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("KenGen.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Kenya Power and Lighting Ltd (KPLC)***"
                name1="Kenya Power"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=KPLC"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("KPLC.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Total Kenya Ltd (TOTL)***"
                name1="Total Kenya"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=TOTL"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("TotalKenya.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Umeme Limited (UMME)***"
                name1="Umeme"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=UMME"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("Umeme.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")
                import shutil
                import glob
                path = r'C:\Users\USER\Desktop\Day to day AI\Nomeon\Media\Financial Data\Industries\NSE'
                allFiles = glob.glob(path + "/*.csv")
                with open('Energy.csv', 'wb') as outfile:
                    for i, fname in enumerate(allFiles):
                        with open(fname, 'rb') as infile:
                            if i != 0:
                                infile.readline()  # Throw away header on all but first file
                                # Block copy rest of file from input to output without parsing
                            shutil.copyfileobj(infile, outfile)
                            print(fname + " has been imported.")
                            print("\n")

            if jibu=="7":
                print("\n")
                print("Insurance Companies ")
                print("Generating data.....")
                print("\n")
                name="***Britam Holdings Ltd (BRIT)***"
                name1="Britam"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=BRIT"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("Britam.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***CIC Insurance Group Ltd (CIC)***"
                name1="CIC"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=CIC"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("CIC.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Jubilee Holdings Ltd (JUB)***"
                name1="JubileeHoldings"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=JUB"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("Jubilee.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Kenya Re-Insurance Corporation Ltd (KNRE)***"
                name1="KenyaRe"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=KNRE"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("KenyaRe.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Liberty Kenya Holdings Ltd (CFCI)***"
                name1="LibertyKenya Holdings"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=CFCI"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("LibertyKenya.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Sanlam Kenya Plc (PAFR)***"
                name1="Sanlam"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=PAFR"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("Sanlam.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")
                import shutil
                import glob
                path = r'C:\Users\USER\Desktop\Day to day AI\Nomeon\Media\Financial Data\Industries\NSE'
                allFiles = glob.glob(path + "/*.csv")
                with open('Insurance.csv', 'wb') as outfile:
                    for i, fname in enumerate(allFiles):
                        with open(fname, 'rb') as infile:
                            if i != 0:
                                infile.readline()  # Throw away header on all but first file
                                # Block copy rest of file from input to output without parsing
                            shutil.copyfileobj(infile, outfile)
                            print(fname + " has been imported.")
                            print("\n")

            if jibu=="8":
                print("\n")
                print("Investment companies ")
                print("Generating data.....")
                print("\n")
                name="***Centum Investment Company Ltd (ICDC)***"
                name1="Centum"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=ICDC"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("Centum.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Home Afrika Ltd (HAFR)***"
                name1="HomeAfrica"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=HAFR"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("HomeAfrica.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Kurwitu Ventures Ltd (KURV)***"
                name1="Kurwitu"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=KURV"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("Kurwitu.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")
                
                print("\n")
                name="***Olympia Capital Holdings Ltd (OCH)***"
                name1="Olympia Capital"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=OCH"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("Olympia.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Trans-Century Ltd (TCL)***"
                name1="Transcentury"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=TCL"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("Transcentury.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")
                import shutil
                import glob
                path = r'C:\Users\USER\Desktop\Day to day AI\Nomeon\Media\Financial Data\Industries\NSE'
                allFiles = glob.glob(path + "/*.csv")
                with open('InvestmentCompanies.csv', 'wb') as outfile:
                    for i, fname in enumerate(allFiles):
                        with open(fname, 'rb') as infile:
                            if i != 0:
                                infile.readline()  # Throw away header on all but first file
                                # Block copy rest of file from input to output without parsing
                            shutil.copyfileobj(infile, outfile)
                            print(fname + " has been imported.")
                            print("\n")

            if jibu=="9":
                print("\n")
                print("Generating data.....")
                print("\n")
                name="***Nairobi Securities Exchange Plc (NSE)***"
                name1="NSE"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=NSE"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("NSE.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")
                import shutil
                import glob
                path = r'C:\Users\USER\Desktop\Day to day AI\Nomeon\Media\Financial Data\Industries\NSE'
                allFiles = glob.glob(path + "/*.csv")
                with open('InvestmentServices.csv', 'wb') as outfile:
                    for i, fname in enumerate(allFiles):
                        with open(fname, 'rb') as infile:
                            if i != 0:
                                infile.readline()  # Throw away header on all but first file
                                # Block copy rest of file from input to output without parsing
                            shutil.copyfileobj(infile, outfile)
                            print(fname + " has been imported.")
                            print("\n")

            if jibu=="10":
                print("\n")
                print("Manufacturing and Allied Companies")
                print("Generating data.....")
                print("\n")
                name="***BOC Kenya Ltd (BOC)***"
                name1="BOCKenya"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=BOC"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("BOC.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***British American Tobacco Kenya Ltd (BAT)***"
                name1="BATKenya"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=BAT"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("BAT.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Carbacid Investments Ltd (CARB)***"
                name1="Carbacid"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=CARB"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("Carbacid.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***East African Breweries Ltd (EABL)***"
                name1="EABL"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=EABL"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("EABL.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Flame Tree Group Holdings Ltd (FTGH)***"
                name1="FlameTree"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=FTGH"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("FlameTree.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Kenya Orchards Ltd (ORCH)***"
                name1="Kenya Orchards"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=ORCH"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("Kenya Orchards.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***Mumias Sugar Company Ltd (MSC)***"
                name1="Mumias"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=MSC"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("Mumias.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")

                print("\n")
                name="***UNGA***"
                name1="Unga"
                print(name)
                quote_page = "https://live.mystocks.co.ke/stock=UNGA"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print("\n")
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)
                
                import csv
                with open("UngaGroup.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name1
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("********************")
                import shutil
                import glob
                path = r'C:\Users\USER\Desktop\Day to day AI\Nomeon\Media\Financial Data\Industries\NSE'
                allFiles = glob.glob(path + "/*.csv")
                with open('Manufacturing.csv', 'wb') as outfile:
                    for i, fname in enumerate(allFiles):
                        with open(fname, 'rb') as infile:
                            if i != 0:
                                infile.readline()  # Throw away header on all but first file
                                # Block copy rest of file from input to output without parsing
                            shutil.copyfileobj(infile, outfile)
                            print(fname + " has been imported.")
                            print("\n")

        if choice =="2":
            print("Pick an Index.")
            print("1. NSE All Share Index.")
            print("2. NSE 20 Share Index.")
            print("3. NSE 25 Share Index.")
            print("\n")
            ans=input("Your Pick? ")
            
            if ans =="1":
                quote_page = "https://live.mystocks.co.ke/stock=%5ENASI"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")

                name="NSE All Share Index"
                print("****", name, "****")
                print("\n")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)

                import csv
                #open a csv file with append, so old data will not be erased
                with open("NSEAllShare-Index.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("\n")
                print("********************")

            if ans=="2":
                quote_page = "https://live.mystocks.co.ke/stock=%5EN20I"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")

                name="NSE 20-Share Index"
                print("****", name, "****")
                print("\n")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print(name_box2.text)
                print("Current Price: ", name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price: ", name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)

                import csv
                #open a csv file with append, so old data will not be erased
                with open("NSE20Share-Index.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("\n")
                print("********************")

            if ans=="3":
                quote_page = "https://live.mystocks.co.ke/stock=%255EN25I"
                page = urllib.request.urlopen(quote_page)
                soup = BeautifulSoup(page, "lxml")

                name="NSE 25-Share Index"
                print("****", name, "****")
                print("\n")
                name_box1 = soup.find("b", attrs={"id": "rtPrev"})
                name_box2 = soup.find("div", attrs={"id": "rtTime"})
                name_box3 = soup.find("div", attrs={"id": "rtPrice"})
                name_box4 = soup.find("div", attrs={"id": "rtChange"})
                print(name_box2.text)
                print(name_box3.text)
                Currentprice=name_box3.text
                print("Previous Price")
                print(name_box1.text)
                previousPrice=name_box1.text
                print("Change: ", name_box4.text)

                import csv
                #open a csv file with append, so old data will not be erased
                with open("NSE25Share-Index.csv", "a", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Name",  "Current", "Previous", "Change"])
                    Name=name
                    
                    Current= Currentprice
                    Previous=previousPrice
                    Change=name_box4.text
                    writer.writerow([Name, Current, Previous, Change])
                print("\n")
                print("********************")
                if __name__ == "__main__":
                    main()
            if __name__ == "__main__":
                main()
        if __name__ == "__main__":
            main()
    if __name__ == "__main__":
        main()
if __name__ == "__main__":
    main()            

