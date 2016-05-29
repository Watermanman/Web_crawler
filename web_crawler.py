import re,threading
import queue
import requests
import sys
import time
links=[]
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
        print("New Link=>{}".format(self.url))
        link_re=re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-f]))+') 
        #link_re=re.compile('href="(.*?)"')
        email_re=re.compile('([\w\.,]+@[\w\.,]+\.\w+)')
        req=requests.get(self.url)
        if req.status_code == 200:
            getlinks=link_re.findall(req.text)
            #links2=re.search(link_re,req.text)
            getemails=email_re.findall(req.text)

            for i in getemails:
                if i in emails:
                    continue
                else:
                    emails.append(i)
            #print("===========Links===============")
            for i in getlinks:
                if i in links:
                    continue
                else:
                    links.append(i)
                    #print("start to "+i)
                    Newlink(i,cond).start()
            self.cond.release()
            print("===========Email===============") 
            for i in emails:
                print(i)
        else:
            self.cond.release()
            print("done")
        
if __name__ == "__main__":

    url=input("Please enter url(defult=www.google.com.tw):") 
    if url == "":
        url="https://www.google.com.tw/" 
    Newlink(url,cond).start()  
    # time.sleep(3) 
    # print (len(links))
    # for i in links:
    #     Newlink(i,cond).start()
    # time.sleep(5)
    # print (len(links))
