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

            req = requests.Session()

            length = 524 + len(word)
            header = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Content-Length": str(length),
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "apps.sd.gov",
                "Origin": "https://apps.sd.gov",
                "Referer": "https://apps.sd.gov/RV66Renewals/checkplates/checkplates.aspx",
                "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
            }
            data = {
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                "__VIEWSTATE": "/wEPDwUKMTYxNTE4MjI4NmRkgwVmYYG+VnM+kmN8FfooxALHGWiJP3txut2GQflHfkw=",
                "__VIEWSTATEGENERATOR": "FCEECA1C",
                "__SCROLLPOSITIONX": "0",
                "__SCROLLPOSITIONY": "0",
                "__EVENTVALIDATION": "/wEdAAPZtIjvWROi77RZL4avqfwvUDCWYx1NqSrZSFbnI4tQhrklmf8tmrtbcNI/Lk8ztU7LW0W180fFFpS6baThHzrL15Zz/RSQE362aDVqFOof3w==",
                "ctl00$ContentPlaceHolder1$txtPlate": word,
                "ctl00$ContentPlaceHolder1$btnCheck": "Check"
            }
            response = req.post(url="https://apps.sd.gov/RV66Renewals/checkplates/checkplates.aspx", data=data, headers=header)

            if "not in use" in response.text:
                print(colored("PLATE AVAILABLE:  " + word, 'green'))
                f = open("outputresults.txt", "a")
                f.write(word + "\n")
                f.close()
            else:
                print(colored("PLATE UNAVAILABLE:  " + word, 'red'))


if __name__ == '__main__':
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
