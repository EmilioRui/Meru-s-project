import csv
# import logging
import random
import string

from anticaptchaofficial.recaptchav2proxyless import *
from bs4 import BeautifulSoup
from requests_toolbelt import MultipartEncoder
from threading import Thread
from queue import Queue


"""domanda: i chaptcha devono essere per forza dentro quei cicli o li posso mettere anche fuori? """

# 
# # try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1
#
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

n_captha = 50   #numero di captcha da ottenere durante un programma


def solve_captcha(queue):
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

    with open('Stat1.csv') as file:
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            if count == 0:
                print("Pagina Caricata")
                count += 1

            proxies = {
                "http": "http://" + row['User'] + ":" + row['Auth'] + "@" + row['IP'] + ":" + row['Port'] + "/",
                "https": "http://" + row['User'] + ":" + row['Auth'] + "@" + row['IP'] + ":" + row['Port'] + "/"
            }

            headers1 = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
            }

            with requests.Session() as session:
                url = 'https://www.statuto18.com/DunkHighMaizeBlue'

                res = requests.get(url, proxies=proxies, headers=headers1)
                soup = BeautifulSoup(res.text, 'html.parser')

                day = soup.select_one('input.form-control:nth-child(3)').get('name')
                month = soup.select_one('input.form-control:nth-child(4)').get('name')
                year = soup.select_one('input.form-control:nth-child(5)').get('name')
                cf = soup.select_one('input.form-control:nth-child(9)').get('name')

                if not day or not month or not year or not cf:
                    print("Empty field: day/month/year/cf")
                    continue


                # solver = recaptchaV2Proxyless()
                # solver.set_verbose(1)
                # solver.set_key("bef80b4f70976b0452b83cddf6f9b152")
                # solver.set_website_url(url)
                # solver.set_website_key("6LdrtrgUAAAAAAAio3UhHrVdJUQXpP3vfbcFm3qx")
                # g_response = solver.solve_and_return_solution()
                # if g_response != 0:
                #     print("g-response: " + g_response)
                # else:
                #     print("task finished with error " + solver.error_code)

                g_response = queue.get()
                form_data = {
                    'nome2': row['Nome'],
                    'cognome2': row['Cognome'],
                    day: row['Giorno'],
                    month: row['Mese'],
                    year: row['Anno'],
                    'telefono2': row['Telefono'],
                    'email2': row['Mail'],
                    'email_conf2': row['Mail'],
                    cf: row['CF'],
                    'comune2': row['Comune'],
                    'provincia2': row['Provincia'],
                    'paese2': 'IT',
                    'sesso2': row['Sesso'],
                    'taglia2': row['Taglia'],
                    'check2': 'S',
                    'captcha2': 'undefined',
                    'campagna2': 'DunkHighMaizeBlue',
                    'form': 'registra',
                    'mark': 'S',
                    'cessione': 'S',
                    'g-recaptcha-response': g_response,
                    'action': 'trueins'
                }

                m = MultipartEncoder(fields=form_data, boundary='----WebKitFormBoundary' + ''.join(
                    random.sample(string.ascii_letters + string.digits, 16)))

                headers2 = {
                    "Content-Type": m.content_type,
                    'Cookie': 'PHPSESSID=' + res.cookies.get('PHPSESSID'),
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
                }

                # print(form_data)

                r = session.post(url, data=m, headers=headers2, proxies=proxies)

                soup = BeautifulSoup(r.text, 'lxml')
                thank = soup.find("div", id="content-thankyou")
                if thank==None:
                    print(row['Mail'], "non entrata")
                    text_file = open("ST1.txt", "a")
                    text_file.write(row['Cognome'])
                    text_file.write('\n')
                    text_file.close()
                else:
                    print(row['Mail'], "DENTRO")



queue = Queue(maxsize = 0 )     #questa è la coda dove ci saranno i chaptcha teoricamente 
n_threads = 100              #numero di processi che vuoi in parallelo

if name == if __name__ == "__main__":
    for i in range(n_threads):
        # if i == 10:     #cosi scegli quale thread dedicare al main
        #     work = Thread (target= main())
        # else:
        t = Thread(target = solve_captcha, args = (queue,))
        t.setDaemon(True)
        t.start()

    main()
