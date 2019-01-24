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
from collections import OrderedDict
import os
from peewee import *
from win10toast import ToastNotifier
from pytrends.request import TrendReq

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
now = datetime.now()
toaster = ToastNotifier()

print("Taarifa® [Version 1.2] |  Promoting fact-checking and news literacy. ")
copyright_=input("Type 'copyright' for more information, or press 'enter' to continue:- ")
if copyright_ =="copyright":
    print("Copyright © 2019 wakili.ai | All Rights Reserved.")
print("\n")

def main():
    print("Choose a command. ")
    print("1. News Digest.\n2. Mercury - Fake News Monitor .\n3. Trends - Keyword search trends . ")
    print("\n")
    mat=input("Choice: ")
    print("\n")
    print("-" *35)
    req = Request("https://www.google.com/ ")
    try:
        response = urlopen(req)
    except URLError as e:
        print("Taarifa requires an internet connection. ")
        print("Please check and try again.")
        if __name__ == "__main__":
            main()
            
    if mat=="3":
        SearchTrend=input("Give me a word and i'll gather its search trends for you: ")
        toaster.show_toast("Taarifa Trends.",
                                    "A simple way to gather keyword search frequency. ",
                                    icon_path="newscon.ico",
                                    duration=5)
        pytrend = TrendReq()
        pytrend.build_payload(kw_list=[SearchTrend])
        related_queries_dict = pytrend.related_queries()

        print(related_queries_dict)
        print("\n")
        if __name__ == "__main__":
            main()
        
        
    if mat=="2":
        toaster.show_toast("Taarifa Mercury spots fake news with AI.",
                            " ",
                            icon_path="newscon.ico",
                            duration=5)
        url_= input("Please paste the article's link in full: ")
        import validators
        validators.url(url_)
        if not validators.url(url_):
            print("\n")
            print("✘That's an invalid link :( Try again. ")
            print("\n")
            main()
        else:
            print("\n")
            print("✔ Link validated. Now analysing article...")
            article = Article(url_)
            article.download()
            article.html
            article.parse()
            
            print("\n")
            print("Author(s): ", article.authors)
            print("\n")
            print("Date of Publication: ", article.publish_date)
            print("\n")

            blob=TextBlob(article.text)
            subjectivity= blob.sentiment.subjectivity
            blob= TextBlob(article.text, analyzer = NaiveBayesAnalyzer())
            positive= blob.sentiment.p_pos
            negative= blob.sentiment.p_neg
            list=textwrap3.wrap(article.text, width=95)
            for element in list:
                print(element)
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
            elif subjective>=extreme_bias:
                print("***Reliability***")
                print("Read with extreme caution. Misinformation traces detected.")    
            print("-" *35)


    if mat=="1":
        # Set the limit for number of articles to download
        LIMIT = 5
        data = {}
        data['newspapers'] = {}
        toaster.show_toast("Digest in progress ",
                            "You can stay and watch or do some work then come back :) ",
                            icon_path="newscon.ico",
                            duration=5)
        time.sleep(1)
        
        # Loads the JSON files with news sites
        with open('News.json') as data_file:
            companies = json.load(data_file)
        for company, value in companies.items():
            print("'", company, "'")
            count = 1
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
                article['author']=content.authors
                article['summary']=content.summary
                article['date']=content.publish_date
                newsPaper['articles'].append(article)
                
                blob=TextBlob(content.text)
                subjectivity= blob.sentiment.subjectivity
                blob= TextBlob(content.text, analyzer = NaiveBayesAnalyzer())
                positive= blob.sentiment.p_pos
                negative= blob.sentiment.p_neg
                    
                print(count, ")", content.title)
                print("\n")
                print("Author(s): ", content.authors)
                print("\n")
                print("Date of Publication: ", content.publish_date)
                print("\n")
                list=textwrap3.wrap(content.summary, width=95)
                for element in list:
                    print(element.translate(non_bmp_map))
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
                elif subjective>=extreme_bias:
                    print("***Reliability***")
                    print("Read with extreme caution. Misinformation traces detected.")
                    
                print("-" *35)
                print("\n")
                count = count + 1
                noneTypeCount = 0
                data['newspapers'][company] = newsPaper
                import csv                    
                with open('Taarifa_Digest.csv', 'a', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(['Company', "Author", "Date", "Title", 'Text', 'Link', "Reliability"])
                    Company=company
                    Author= article['author']
                    Date=article['date']
                    Title= article['title']
                    Text= article['text']
                    Link= article['link']
                    Reliability=round(subjectivity)
                    writer.writerow([Company, Author, Date, Title, Text, Link, Reliability])
    main()
if __name__ == "__main__":
    main()

