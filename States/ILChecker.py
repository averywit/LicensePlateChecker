import requests
import multiprocessing
from termcolor import colored
from colorama import init
init(autoreset=True)


class Worker(multiprocessing.Process):

    def __init__(self, job_queue):
        super().__init__()
        self._job_queue = job_queue

    def run(self):
        while True:
            word = self._job_queue.get()
            if word is None:
                break

            try:

                proxies = {
                    # INSERT PROXIES HERE "http": "",
                    # INSERT PROXIES HERE "https": ""
                }

                req = requests.Session()

                header1 = {
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.9",
                    "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "macOS",
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "none",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
                response = req.get(url="https://apps.ilsos.gov/pickaplate/", headers=header1, proxies=proxies)

                header2 = {
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.9",
                    "cache-control": "max-age=0",
                    "content-length": "23",
                    "content-type": "application/x-www-form-urlencoded",
                    "origin": "https://apps.ilsos.gov",
                    "referer": "https://apps.ilsos.gov/pickaplate/",
                    "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "macOS",
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
                }
                data1 = {
                    "command": "index",
                    "pltType": "1"
                }
                response = req.post(url="https://apps.ilsos.gov/pickaplate/pickaplate", data=data1, headers=header2, proxies=proxies)

                chewy = str(response.text)
                chewy = chewy[15643:15655]
                chewy1 = chewy.replace('"', '')
                chewy2 = chewy1.replace('>', '')
                chewy3 = chewy2.replace('=', '')
                chewy4 = chewy3.strip()

                header3 = {
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.9",
                    "cache-control": "max-age=0",
                    "content-length": "92",
                    "content-type": "application/x-www-form-urlencoded",
                    "origin": "https://apps.ilsos.gov",
                    "referer": "https://apps.ilsos.gov/pickaplate/pickaplate",
                    "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "macOS",
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
                }
                data2 = {
                    "chewy": chewy4,
                    "command": "availability",
                    "pltType": "1",
                    "plateType": "1",
                    "pltWant": "",
                    "chosen": "yes",
                    "a": "1",
                    "lpNum": word
                }
                response = req.post(url="https://apps.ilsos.gov/pickaplate/pickaplate", data=data2, headers=header3, proxies=proxies)

                if "Congratulations!  <b>" in str(response.content):
                    print(colored("PLATE AVAILABLE:  " + word, 'green'))
                    f = open("outputresults.txt", "a")
                    f.write(word + "\n")
                    f.close()
                else:
                    print(colored("PLATE UNAVAILABLE:  " + word, 'red'))

            except:
                self._job_queue.put(word)


if __name__ == '__main__':
    f1 = open("outputresults.txt", "w")

    # On-screen input for desired checks
    print("1 <- All 1 letter/character combinations")
    print("2 <- All 2 letter combinations")
    print("3 <- All 3 letter combinations")
    print("4 <- All 3 letter words")
    print("5 <- All 4 letter words")
    print("6 <- All 5 letter words")
    print("7 <- All 3+4 numbers")
    choice = int(input("Please enter what you want to check: "))

    lines = []
    random = 0
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
                "V", "W", "X", "Y", "Z"]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    index = 0
    stupidparse = ""
    # Creating an array of all the 1 letter/character combinations
    if choice == 1:
        for i in alphabet:
            lines.insert(index, i)
            index += 1
        for i in numbers:
            lines.insert(index, i)
            index += 1
    # Creating an array of all 2 letter combinations
    if choice == 2:
        for i in alphabet:
            for j in alphabet:
                lines.insert(index, i + j)
                index += 1
        for l in numbers:
            for m in numbers:
                lines.insert(index, l + m)
                index += 1
    # Creating an array of all 3 letter combinations
    elif choice == 3:
        for i in alphabet:
            for j in alphabet:
                for k in alphabet:
                    lines.insert(index, i + j + k)
                    index += 1
    # Retrieving the list of all 3 letter words from Github scrape
    elif choice == 4:
        url = "https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/3letterwords.txt"
        r = requests.get(url)
        for line in r.iter_lines():
            if line:
                lines.insert(index, str(line).strip("b'"))
                index += 1
    # Retrieving the list of all 4 letter words from Github scrape
    elif choice == 5:
        url = "https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/4letterwords.txt"
        r = requests.get(url)
        for line in r.iter_lines():
            if line:
                stupidparse = str(line)
                lines.insert(index, stupidparse[2:6])
                index += 1
    # Retrieving the list of all 5 letter words from Github scrape
    elif choice == 6:
        url = "https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/5letterwords.txt"
        r = requests.get(url)
        for line in r.iter_lines():
            if line:
                stupidparse = str(line)
                lines.insert(index, stupidparse[2:7])
                index += 1

    # Creating an array of all 3 number combinations
    elif choice == 7:
        for l in numbers:
            for m in numbers:
                for n in numbers:
                    lines.insert(index, l + m + n)
                    index += 1

    jobs = []
    job_queue = multiprocessing.Queue()

    for i in range(10):
        p = Worker(job_queue)
        jobs.append(p)
        p.start()

    for line in lines:
        job_queue.put(line)

    for j in jobs:
        job_queue.put(None)

    for j in jobs:
        j.join()
