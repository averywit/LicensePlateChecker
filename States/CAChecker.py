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

                session = requests.Session()

                headers1 = {
                    "Sec-Ch-Ua": "\"Chromium\";v=\"105\", \"Not)A;Brand\";v=\"8\"",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Sec-Ch-Ua-Platform": "\"Windows\"",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-Dest": "document",
                    "Accept-Encoding": "gzip, deflate",
                    "Sec-Fetch-Mode": "navigate",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-User": "?1",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Sec-Ch-Ua-Mobile": "?0"
                }
                session.get("https://www.dmv.ca.gov/wasapp/ipp2/initPers.do", headers=headers1, proxies=proxies)

                data2 = {
                    "acknowledged": "true",
                    "_acknowledged": "on"
                }
                headers2 = {
                    "Origin": "https://www.dmv.ca.gov",
                    "Sec-Ch-Ua": "\"Chromium\";v=\"105\", \"Not)A;Brand\";v=\"8\"",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Sec-Ch-Ua-Platform": "\"Windows\"",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36",
                    "Referer": "https://www.dmv.ca.gov/wasapp/ipp2/initPers.do", "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate",
                    "Sec-Fetch-Mode": "navigate",
                    "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-User": "?1",
                    "Accept-Language": "en-US,en;q=0.9", "Sec-Ch-Ua-Mobile": "?0",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
                session.post("https://www.dmv.ca.gov/wasapp/ipp2/startPers.do", data=data2, headers=headers2, proxies=proxies)

                data3 = {
                    "imageSelected": "none",
                    "licPlateReplaced": "8JBZ269",
                    "isRegExpire60": "no",
                    "plateType": "R",
                    "last3Vin": "695",
                    "isVehLeased": "no",
                    "vehicleType": "AUTO"
                }
                headers3 = {
                    "Origin": "https://www.dmv.ca.gov",
                    "Sec-Ch-Ua": "\"Chromium\";v=\"105\", \"Not)A;Brand\";v=\"8\"",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Sec-Ch-Ua-Platform": "\"Windows\"",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36",
                    "Referer": "https://www.dmv.ca.gov/wasapp/ipp2/startPers.do",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate",
                    "Sec-Fetch-Mode": "navigate",
                    "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-User": "?1",
                    "Accept-Language": "en-US,en;q=0.9", "Sec-Ch-Ua-Mobile": "?0",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
                session.post("https://www.dmv.ca.gov/wasapp/ipp2/processPers.do", data=data3, headers=headers3, proxies=proxies)

                if len(word) == 7:
                    formatted = list(word.upper())
                else:
                    formatted = list(word.upper())
                    check = 7 - len(word)
                    count = 0
                    while count < check:
                        formatted.append("")
                        count = count + 1

                data4 = {
                    "plateLength": "7",
                    "kidsPlate": "",
                    "plateType": "R",
                    "plateNameLow": "environmental",
                    "plateChar6": str(formatted[6]),
                    "plateChar5": str(formatted[5]),
                    "plateChar4": str(formatted[4]),
                    "plateChar3": str(formatted[3]),
                    "plateChar2": str(formatted[2]),
                    "plateChar1": str(formatted[1]),
                    "plateChar0": str(formatted[0])
                }
                headers4 = {
                    "Origin": "https://www.dmv.ca.gov",
                    "Sec-Ch-Ua": "\"Chromium\";v=\"105\", \"Not)A;Brand\";v=\"8\"",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Sec-Ch-Ua-Platform": "\"Windows\"",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36",
                    "Referer": "https://www.dmv.ca.gov/wasapp/ipp2/processPers.do",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate",
                    "Sec-Fetch-Mode": "navigate",
                    "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-User": "?1",
                    "Accept-Language": "en-US,en;q=0.9", "Sec-Ch-Ua-Mobile": "?0",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
                response = session.post("https://www.dmv.ca.gov/wasapp/ipp2/processConfigPlate.do", data=data4, headers=headers4, proxies=proxies)

                if "Verification" in str(response.content):
                    print(colored("PLATE AVAILABLE:  " + word, 'green'))
                    f = open("outputresults.txt", "a")
                    f.write(word + "\n")
                    f.close()
                else:
                    print(colored("PLATE UNAVAILABLE:  " + word, 'red'))
            except:
                self._job_queue.put(word)


if __name__ == '__main__':
    # On-screen input for desired checks
    print("1 <- All 1 letter/character combinations")
    print("2 <- All 2 letter combinations")
    print("3 <- All 3 letter combinations")
    print("4 <- All 3 letter words")
    print("5 <- All 4 letter words")
    print("6 <- All 5 letter words")
    print("7 <- All 3 numbers")
    print("8 <- All 3-4 letter repeaters")
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
            for k in numbers:
                lines.insert(index, i + k)
                index += 1
        for l in numbers:
            for m in numbers:
                lines.insert(index, l + m)
                index += 1
            for n in alphabet:
                lines.insert(index, l + n)
    # Creating an array of all 3 letter combinations
    elif choice == 3:
        for i in alphabet:
            for j in alphabet:
                for k in alphabet:
                    if index > 14873:
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

    # Creating an array of all 3 letter combinations
    elif choice == 7:
        for i in numbers:
            for j in numbers:
                for k in numbers:
                    lines.insert(index, i + j + k)
                    index += 1

    # Creating an array of all 3 letter combinations
    elif choice == 8:
        for i in alphabet:
            lines.insert(index, i + i + i)
            index += 1
        for j in alphabet:
            lines.insert(index, j + j + j + j)
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
