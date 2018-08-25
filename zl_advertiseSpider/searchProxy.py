# encoding: utf-8
"""
Spider ip proxy. Website: http://www.xicidaili.com/nn
"""

from bs4 import BeautifulSoup
import urllib3
import time
import socket
import random

def getContent(Url):
    """ Get the web site content.  """


    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'}
    http = urllib3.PoolManager(headers=header)

    while True:
        try:
            response = http.request(url=Url,method='get').data       # request
            break
        except urllib3.exceptions as e:     # Ouput log to debug easily
            print(1, e)
            time.sleep(random.choice(range(5, 20)))
        except socket.timeout as e:
            print(2, e)
            time.sleep(random.choice(range(15, 20)))
        except Exception as e:
            print(3, e)
            time.sleep(random.choice(range(10, 20)))

    return response                       # The website content

def extractIPAddress(content):
    """ Extract web IP address and port. """
    proxys = []                                   # proxy list
    soup = BeautifulSoup(content, 'html.parser')  # soup object
    trs = soup.find_all('tr')                     # extract tr tag
    for tds in trs[1:]:
        td = tds.find_all('td')                   # extract td tag
        if td[5].contents[0] == 'HTTPS':
            continue
        proxys.append(str(td[5].contents[0]+"://"+td[1].contents[0]) + ":" + str(td[2].contents[0]))

    return proxys

def getProxys():
    """ main function. """
    Url = 'http://www.xicidaili.com/nn/1'   # assign relevant url
    content = getContent(Url)               # achieve html content
    proxys = extractIPAddress(content)      # achieve proxys
    # for e in proxys:                        # output proxy on screen
    #     print e

    return proxys