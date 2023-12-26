import re
import requests
import threading
from termcolor import colored
from colorama import init
from queue import Queue
init(autoreset=True)


class Worker(threading.Thread):

    def __init__(self, job_queue, max_retries=10):
        super().__init__()
        self._job_queue = job_queue
        self._max_retries = max_retries

    def run(self):
        while True:
            word = self._job_queue.get()
            if word is None:
                break

            retries = 0
            while retries < self._max_retries:
                try:
                    session = requests.session()
                    response = session.get(
                        url="https://expresslane.dps.louisiana.gov/plate/plate2.aspx",
                        timeout=10
                    )

                    reload_secret = re.search(r'name="ctl00\$ctl00\$hidReloadSecret"[\s\S]*?value="([^"]*)"', response.text).group(1)
                    if reload_secret != "now":
                        reload_secret = "then"
                    else:
                        reload_secret = "now"

                    data = {
                        '__LASTFOCUS': '',
                        '__VIEWSTATE': re.search(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="([^"]*)" />', response.text).group(1),
                        '__VIEWSTATEGENERATOR': re.search(r'<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="([^"]*)" />', response.text).group(1),
                        '__EVENTTARGET': "",
                        '__EVENTARGUMENT': "",
                        '__EVENTVALIDATION': re.search(r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="([^"]*)" />', response.text).group(1),
                        'cx': "017344992912482891441:flho9n5gxim",
                        "cof": "FORID:10",
                        "ie": "UTF-8",
                        "q": "search motor vehicles",
                        "ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$txtPlate": word,
                        "ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$btnSubmit": "Submit",
                        "ctl00$ctl00$hidReloadSecret": reload_secret
                    }
                    response = session.post(
                        url="https://expresslane.dps.louisiana.gov/plate/plate2.aspx",
                        data=data,
                        timeout=10
                    )

                    if response.status_code == 200:
                        if f'<span id="ContentPlaceHolder1_ContentPlaceHolder1_lblResults"><font face="Arial" color="#0000FF">The personalized plate <b>{word}</b> is available.<br><br><a style="color: blue;" href="https://dpsweb.dps.louisiana.gov/omvprestigeplaterequest.nsf/request?OpenForm&Choice1={word}">Request this personalized plate!</a></font></span>' in response.text:
                            print(colored("PLATE AVAILABLE:  " + word, 'green'))
                            f = open("outputresults.txt", "a")
                            f.write(word + "\n")
                            f.close()
                        else:
                            print(colored("PLATE UNAVAILABLE:  " + word, 'red'))
                        break

                except:
                    retries += 1


def generateCombinations(input_number):

    # Used for combination generation
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"

    # Creating a list of all 1-character combinations
    if input_number == 1:
        return [
            *[a for a in alphabet],
            *[b for b in alphabet]
        ]

    # Creating a list of all 3-character combinations
    elif input_number == 2:
        return [
            *[a + b for a in alphabet for b in alphabet],
            *[a + b for a in alphabet for b in numbers],
            *[a + b for a in numbers for b in numbers]
        ]

    # Creating a list of all 3-letter combinations
    elif input_number == 3:
        return [a + b + c for a in alphabet for b in alphabet for c in alphabet]

    # Creating a list of all 3-number combinations
    elif input_number == 4:
        return [a + b + c for a in numbers for b in numbers for c in numbers]

    # Creating a list of all 3-letter words via GitHub scrape
    elif input_number == 5:
        return requests.get(
            url="https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/3letterwords.txt"
        ).text.split("\n")

    # Creating a list of all 4-letter words via GitHub scrape
    elif input_number == 6:
        return requests.get(
            url="https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/4letterwords.txt"
        ).text.split("\n")

    # Creating a list of all 5-letter words via GitHub scrape
    elif input_number == 7:
        return requests.get(
            url="https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/5letterwords.txt"
        ).text.split("\n")

    # Creating a list of all 3, 4, 5-letter repeater combinations
    elif input_number == 8:
        return [
            *[a + a + a for a in alphabet],
            *[a + a + a + a for a in alphabet],
            *[a + a + a + a + a for a in alphabet]
        ]


if __name__ == '__main__':

    # On-screen input for desired checks
    print("1 <- All 1 character combinations")
    print("2 <- All 2 letter combinations")
    print("3 <- All 3 letter combinations")
    print("4 <- All 3 number combinations")
    print("5 <- All 3 letter word combinations")
    print("6 <- All 4 letter word combinations")
    print("7 <- All 5 letter word combinations")
    print("8 <- All 3, 4, 5 letter repeater combinations")
    choice = int(input("Please enter what you want to check: "))

    # Holds the combinations to check
    combinations = generateCombinations(choice)

    jobs = []
    job_queue = Queue()

    for i in range(25):
        p = Worker(job_queue)
        jobs.append(p)
        p.start()

    for combo in combinations:
        job_queue.put(combo)

    for j in jobs:
        job_queue.put(None)

    for j in jobs:
        j.join()
