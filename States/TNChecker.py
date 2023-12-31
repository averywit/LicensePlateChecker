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
                    session = requests.Session()
                    header = {
                        "accept": "application/json, text/javascript, */*; q=0.01",
                        "accept-encoding": "gzip, deflate, br",
                        "accept-language": "en-US,en;q=0.9",
                        "connection": "keep-alive",
                        "content-length": str(83+len(word)),
                        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "origin": "https://personalizedplates.revenue.tn.gov",
                        "referer": "https://personalizedplates.revenue.tn.gov/",
                        "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
                        "sec-ch-ua-mobile": "?0",
                        "sec-ch-ua-platform": '"macOS"',
                        "sec-fetch-dest": "empty",
                        "sec-fetch-mode": "cors",
                        "sec-fetch-site": "same-origin",
                        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
                        "X-Requested-With": "XMLHttpRequest"
                    }
                    data = {
                        "send[endpoint]": f"/personalizedplates/verifyplate/{word}/3210",
                        "send[type]": "GET"
                    }
                    response = session.post(
                        url="https://personalizedplates.revenue.tn.gov/static/api/api.php",
                        headers=header,
                        data=data,
                        timeout=10
                    )

                    if response.status_code == 200:
                        print(colored("PLATE AVAILABLE:  " + word, 'green'))
                        f = open("outputresults.txt", "a")
                        f.write(word + "\n")
                        f.close()
                        break
                    elif response.status_code == 422:
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
            url="https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/WordLists/3letterwords.txt"
        ).text.split("\n")

    # Creating a list of all 4-letter words via GitHub scrape
    elif input_number == 6:
        return requests.get(
            url="https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/WordLists/4letterwords.txt"
        ).text.split("\n")

    # Creating a list of all 5-letter words via GitHub scrape
    elif input_number == 7:
        return requests.get(
            url="https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/WordLists/5letterwords.txt"
        ).text.split("\n")

    # Creating a list of all 6-letter words via GitHub scrape
    elif input_number == 8:
        return requests.get(
            url="https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/WordLists/6letterwords.txt"
        ).text.split("\n")

    # Creating a list of all 3, 4, 5, 6 repeater combinations
    elif input_number == 9:
        return [
            *[a + a + a for a in alphabet],
            *[a + a + a + a for a in alphabet],
            *[a + a + a + a + a for a in alphabet],
            *[a + a + a + a + a + a for a in alphabet],
            *[a + a + a for a in numbers],
            *[a + a + a + a for a in numbers],
            *[a + a + a + a + a for a in numbers],
            *[a + a + a + a + a + a for a in numbers]
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
    print("8 <- All 6 letter word combinations")
    print("9 <- All 3, 4, 5, 6 repeater combinations")
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
