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
                    headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Content-Length': '153',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'DNT': '1',
                        'Host': 'transactions.dmv.virginia.gov',
                        'Origin': 'https://transactions.dmv.virginia.gov',
                        'Pragma': 'no-cache',
                        'Referer': 'https://transactions.dmv.virginia.gov/dmvnet/plate_purchase/s2end.asp',
                        'Sec-Fetch-Dest': 'frame',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'same-origin',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"macOS"'
                    }
                    data = {
                        'TransID': 'HLDPLT',
                        'HoldISA': 'N',
                        'PltChars': '75',
                        'PltLogoPos': '0',
                        'PltHcapPlt': 'IGWTH',
                        'PltHcapChars': '50',
                        'PltHcapLogoPos': '1',
                        'PltLogoExceptPos': '0',
                        'PltLogoSize': '15',
                        'PltType': 'IGWT',
                        'PltNo': '',
                    }
                    session.post(
                        url="https://transactions.dmv.virginia.gov/dmvnet/plate_purchase/s2dispplt.asp",
                        headers=headers,
                        data=data,
                        timeout=10
                    )

                    headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Content-Length': '296',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Dnt': '1',
                        'Host': 'transactions.dmv.virginia.gov',
                        'Origin': 'https://transactions.dmv.virginia.gov',
                        'Pragma': 'no-cache',
                        'Referer': 'https://transactions.dmv.virginia.gov/dmvnet/plate_purchase/s2end.asp',
                        'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
                        'Sec-Ch-Ua-Mobile': '?0',
                        'Sec-Ch-Ua-Platform': '"macOS"',
                        'Sec-Fetch-Dest': 'frame',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-User': '?1',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
                    }
                    data = {
                        'TransType': 'INQ',
                        'TransID': 'RESINQ',
                        'ReturnPage': '/dmvnet/plate_purchase/s2end.asp',
                        'HelpPage': '',
                        'Choice': 'A',
                        'PltNo': f'{word}',
                        'HoldISA': 'N',
                        'HoldSavePltNo': '',
                        'HoldCallHost': '',
                        'NumCharsInt': '8',
                        'CurrentTrans': 'plate_purchase_reserve',
                        'PltType': 'IGWT',
                        'PltNoAvail': '',
                        'PersonalMsg': 'Y',
                    }
                    for i in range(1, 9):
                        field_name = f'Let{i}'
                        if i <= len(word):
                            data[field_name] = word[i - 1]
                        else:
                            data[field_name] = ''

                    response = session.post(
                        url="https://transactions.dmv.virginia.gov/dmvnet/common/router.asp",
                        headers=headers,
                        data=data,
                        timeout=10
                    )

                    if response.status_code == 200:
                        if "Congratulations" in response.text:
                            print(colored("PLATE AVAILABLE:  " + word, 'green'))
                            f = open("outputresults.txt", "a")
                            f.write(word.strip() + "\n")
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
