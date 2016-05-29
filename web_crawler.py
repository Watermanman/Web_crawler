import re,threading
import queue
import requests
import sys
import time
import os
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
        link_re2=re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-f]))+') 
        link_re=re.compile('href="(.*?)"')
        email_re=re.compile('([\w\.,]+@[\w\.,]+\.\w+)')
        try:
            req=requests.get(self.url)
            if req.status_code == 200:
                getlinks=link_re.findall(req.text)
                getemails=email_re.findall(req.text)

                for i in getemails:
                    if i in emails:
                        continue
                    else:
                        emails.append(i)
                #print("===========Links===============")
                data=open('link_log.txt','a')
                for i in getlinks:
                    chk=re.match("http",i)
                    if chk:
                        if i in links:
                            continue
                        else:
                            links.append(i)
                            data.write(i)
                            data.write('\n')
                            #print("start to "+i)
                            Newlink(i,cond).start()
                    else:
                        newi=self.url+i
                        if newi in links:
                            continue
                        else:
                            links.append(newi)
                            data.write(newi)
                            data.write('\n')
                            #print("start to "+i)
                            Newlink(newi,cond).start()
                data.close()
                self.cond.release()
                print("===========Email===============") 
                data=open('e-mail_log.txt','w')
                for i in emails:
                    data.write(i)
                    data.write("\n")
                    print(i)
                data.close()
            else:
                self.cond.release()
                print("done")
        except requests.exceptions.ConnectionError as e:
            pass
        
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
