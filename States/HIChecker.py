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
                session = requests.Session()
                headers2 = {
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.9",
                    "cache-control": "max-age=0",
                    "connection": "keep-alive",
                    "content-length": "131",
                    "content-type": "application/x-www-form-urlencoded",
                    "host": "www12.honolulu.gov",
                    "origin": "https://www12.honolulu.gov",
                    "referer": "https://www12.honolulu.gov/specialplates/main/frmInquiry.asp?sFlag=search&sType=",
                    "sec-ch-ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"macOS"',
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
                }
                data2 = {}
                if len(word) == 1:
                    data2 = {
                        "txtLicense1": f"{word[0]}",
                        "txtLicense2": "",
                        "txtLicense3": "",
                        "txtLicense4": "",
                        "txtLicense5": "",
                        "txtLicense6": "",
                        "txtLicense7": "",
                        "btnSubmit": "Search",
                        "radType": "on",
                        "txtPlate": f"{word}",
                        "txtPrev": "2"
                    }
                if len(word) == 2:
                    data2 = {
                        "txtLicense1": f"{word[0]}",
                        "txtLicense2": f"{word[1]}",
                        "txtLicense3": "",
                        "txtLicense4": "",
                        "txtLicense5": "",
                        "txtLicense6": "",
                        "txtLicense7": "",
                        "btnSubmit": "Search",
                        "radType": "on",
                        "txtPlate": f"{word}",
                        "txtPrev": "2"
                    }
                if len(word) == 3:
                    data2 = {
                        "txtLicense1": f"{word[0]}",
                        "txtLicense2": f"{word[1]}",
                        "txtLicense3": f"{word[2]}",
                        "txtLicense4": "",
                        "txtLicense5": "",
                        "txtLicense6": "",
                        "txtLicense7": "",
                        "btnSubmit": "Search",
                        "radType": "on",
                        "txtPlate": f"{word}",
                        "txtPrev": "2"
                    }
                if len(word) == 4:
                    data2 = {
                        "txtLicense1": f"{word[0]}",
                        "txtLicense2": f"{word[1]}",
                        "txtLicense3": f"{word[2]}",
                        "txtLicense4": f"{word[3]}",
                        "txtLicense5": "",
                        "txtLicense6": "",
                        "txtLicense7": "",
                        "btnSubmit": "Search",
                        "radType": "on",
                        "txtPlate": f"{word}",
                        "txtPrev": "2"
                    }
                if len(word) == 5:
                    data2 = {
                        "txtLicense1": f"{word[0]}",
                        "txtLicense2": f"{word[1]}",
                        "txtLicense3": f"{word[2]}",
                        "txtLicense4": f"{word[3]}",
                        "txtLicense5": f"{word[4]}",
                        "txtLicense6": "",
                        "txtLicense7": "",
                        "btnSubmit": "Search",
                        "radType": "on",
                        "txtPlate": f"{word}",
                        "txtPrev": "2"
                    }
                response = session.post(url="https://www12.honolulu.gov/specialplates/main/frmInquiry.asp?sFlag=search&sType=", headers=headers2, data=data2)
                if 'class="text-msg-blue">Congratulations!' not in str(response.text):
                    print(colored("PLATE UNAVAILABLE:  " + word, 'red'))
                else:
                    print(colored("PLATE AVAILABLE:  " + word, 'green'))
                    f = open("outputresults.txt", "a")
                    f.write(word + "\n")
                    f.close()

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

    # Creating an array of all 3 + 4 number combinations
    elif choice == 7:
        for i in numbers:
            for j in numbers:
                for k in numbers:
                    lines.insert(index, i + j + k)
                    index += 1
        for i in numbers:
            for j in numbers:
                for k in numbers:
                    for l in numbers:
                        lines.insert(index, i + j + k + l)
                        index += 1

    # Creating an array of all repeater combinations
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
