import mechanize
from bs4 import BeautifulSoup
import os
from Queue import Queue
from threading import Thread
from threading import Semaphore
from urlparse import urljoin

sm = Semaphore(1)
browser = mechanize.Browser()
queue = Queue()
URL = 'http://t0xicra1n.com/linux-forensics-course.html'
DOMAIN = 'http://t0xicra1n.com'

def fileundo():
    with open('Crawler/video.txt','w') as x:
        pass
    with open('Crawler/data.txt','w') as x:
        pass

def worker_thread():
    print "Thread Started Working"
    for _ in range(10):
        t = Thread(target=work)
        t.setDaemon = True
        t.start()

def work():
    while True:
        file2 = open('Crawler/video.txt','a')
        url = queue.get()
        if len(url) > 0:
            print url + " Working"
            try:
                soup = BeautifulSoup(browser.open(url.strip('\n')).read())
            except Exception as ex:
                print url + ' ' + str(ex)
            for lx in soup.find_all('source'):
                vrl = lx.get('src')
                if 'PentesterAcademy' in vrl:
                    sm.acquire()
                    file2.write(urljoin(DOMAIN,vrl) + "\n")
                    sm.release()
            queue.task_done()
        else:
            break;
    file2.close()
def create_job():
    with open('Crawler/data.txt','r') as x:
        for line in x:
            print line.strip('\n')
            queue.put(line.strip('\n'))
    queue.join()

'''
def grabvideos(dirfile,domain):
    file2 = open('Crawler/video.txt','a')
    with open(dirfile, 'r') as x:
        for line in x:
            soup = BeautifulSoup(browser.open(line.strip('\n')).read())
            for lx in soup.find_all('source'):
                vrl = lx.get('src')
                if 'PentesterAcademy' in vrl:
                    file2.write(urljoin(domain,vrl) + "\n")
    file2.close()
'''
def Crawler(url, domain):
    fileundo()
    data = browser.open(url)
    soup = BeautifulSoup(data)
    if not os.path.exists("Crawler"):
        os.makedirs("Crawler")
    file = open('Crawler/data.txt','a')
    nx = 1
    for lx in soup.find_all('a'):
        link = lx.get('href')
        if link is None or 'twitter' in link or 'index' in link or 'tutorials' in link:
            continue
        print str(nx) + ' ' + str(domain) + str(link)
        file.write(urljoin(domain,link) + "\n")
        nx = nx + 1
    file.close()
    worker_thread()
    create_job()
    #grabvideos('Crawler/data.txt', domain)

Crawler(URL,DOMAIN)