import csv
# import logging
import random
import string

from anticaptchaofficial.recaptchav2proxyless import *
from bs4 import BeautifulSoup
from requests_toolbelt import MultipartEncoder
from threading import Thread
from queue import Queue
import threading


queue = Queue(maxsize = 0 )     #questa è la coda dove ci saranno i chaptcha teoricamente 
n_threads = 10              #numero di processi che vuoi in parallelo
url = 'https://www.statuto18.com/DunkHighMaizeBlue'



def solve_captcha(queue, url):
    while True:
        print (threading.current_thread().getName())
        
        solver = recaptchaV2Proxyless()
        solver.set_verbose(1)
        solver.set_key("bef80b4f70976b0452b83cddf6f9b152")
        solver.set_website_url(url)
        solver.set_website_key("6LdrtrgUAAAAAAAio3UhHrVdJUQXpP3vfbcFm3qx")
        g_response = solver.solve_and_return_solution()
        if g_response != 0:
            print("g-response: " + g_response)
            queue.put(g_response)
            queue.task_done
        else:
            print("task finished with error " + solver.error_code)


def main():
    
    for i in range (100):
        print ("_________________SONO NEL MAINNNNN _________________")
        time.sleep(0.2)

    while not queue.empty():

        a = queue.get()
        print (a)
        time.sleep(5)



if __name__ == "__main__":
    for i in range(n_threads):
        """ url e qui sotto!!!!!!!"""
        
        # if i == 10:     #cosi scegli quale thread dedicare al main
        #     work = Thread (target= main())
        # else:
        t = Thread(target = solve_captcha, args = (queue,url, ))
        t.start()
    print ("sono qui!")
    main()
