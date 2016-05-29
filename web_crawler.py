import re,threading
import queue
import requests
import sys
import time

emails=[]
box=queue.Queue(maxsize=10)
cond=threading.Condition()

class Newlink(threading.Thread):

    def __init__(self,url,cond):
        threading.Thread.__init__(self)
        self.url=url
        self.cond=cond

    def run(self):
        self.cond.acquire()
        print("Link={}".format(self.url))
        link_re=re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-f]))+') 
        #link_re=re.compile('href="(.*?)"')
        email_re=re.compile('([\w\.,]+@[\w\.,]+\.\w+)')
        req=requests.get(self.url)
        getlinks=link_re.findall(req.text)
        #links2=re.search(link_re,req.text)
        getemails=email_re.findall(req.text)

        for i in getemails:
            #if i in getemails:
            #    continue
            #else:
            emails.append(i)
        #print("===========Links===============")
        for link in getlinks:
            #print("start to "+k)
            Newlink(link,cond).start()
            #threads.append(Newlink(link))
        self.cond.release()
        print("===========Email===============") 
        for i in emails:
            print(i)

        print("done")
        
if __name__ == "__main__":

    #url=input("Please enter url:") 
    url="https://www.google.com.tw/" 
    Newlink(url,cond).start()  
