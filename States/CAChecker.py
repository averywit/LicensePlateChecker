import requests
import threading
from termcolor import colored
from colorama import init
from queue import Queue
init(autoreset=True)


class Worker(threading.Thread):

    def __init__(self, job_queue, max_retries=10):
        super().__init__()

        # Assigns the job queue to the worker.
        # This is filled with the combinations to check.
        self._job_queue = job_queue

        # Sets the maximum retries (10) for failed requests.
        self._max_retries = max_retries

    def run(self):

        # Runs worker until "None" is reached.
        # None = No combinations are left to check.
        while True:

            # Retreives a combination "word" from "job_queue".
            word = self._job_queue.get()

            # Breaks loop when "None" is retrieved from "job_queue".
            if word is None:
                break

            retries = 0

            # Retry loop that makes multithreading happy.
            # Most of the time, this will not loop. It is just for safety.
            while retries < self._max_retries:
                try:
                    # INSERT RESIDENTIAL PROXIES HERE
                    # ********** REQUIRED ***********
                    proxy_username = ""
                    proxy_password = ""
                    proxy_host = ""
                    proxy_port = ""

                    proxies = {
                        "http": f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
                        "https": f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"
                    }

                    # Assigns proxies to the session for checking the combination.
                    session = requests.session()
                    session.proxies = proxies

                    # Headers for process page 1 in the combination check.
                    headers = {
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

                    # Make the request to get process page 1 in combination check.
                    # Timeout of 10 seconds incase of a bad proxy.
                    session.get(
                        url="https://www.dmv.ca.gov/wasapp/ipp2/initPers.do",
                        headers=headers,
                        timeout=10
                    )

                    # Data for process page 2 in the combination check.
                    data = {
                        "acknowledged": "true",
                        "_acknowledged": "on"
                    }

                    # Headers for process page 2 in the combination check.
                    headers = {
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

                    # Make the request to get process page 2 in combination check.
                    # Timeout of 10 seconds incase of a bad proxy.
                    session.post(
                        url="https://www.dmv.ca.gov/wasapp/ipp2/startPers.do",
                        data=data,
                        headers=headers,
                        timeout=10
                    )

                    # Data for process page 3 in the combination check.
                    data = {
                        "imageSelected": "none",
                        "licPlateReplaced": "8JBZ269",
                        "isRegExpire60": "no",
                        "plateType": "R",
                        "last3Vin": "695",
                        "isVehLeased": "no",
                        "vehicleType": "AUTO"
                    }
                    
                    # Headers for process page 3 in the combination check.
                    headers = {
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

                    # Make the request to get process page 3 in combination check.
                    # Timeout of 10 seconds incase of a bad proxy.
                    session.post(
                        url="https://www.dmv.ca.gov/wasapp/ipp2/processPers.do",
                        data=data,
                        headers=headers,
                        timeout=10
                    )

                    # Reformats the combination "word" to schema required for the request data below.
                    if len(word) == 7:
                        formatted = list(word.upper())
                    else:
                        formatted = list(word.upper())
                        check = 7 - len(word)
                        count = 0
                        while count < check:
                            formatted.append("")
                            count = count + 1

                    # Data for process page 4 in the combination check.
                    data = {
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
                    
                    # Headers for process page 4 in the combination check.
                    headers = {
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

                    # Make the request for process page 4, completing combination check.
                    # Timeout of 10 seconds incase of a bad proxy.
                    response = session.post(
                        url="https://www.dmv.ca.gov/wasapp/ipp2/processConfigPlate.do",
                        data=data,
                        headers=headers,
                        timeout=10
                    )

                    # Successful request, continue to the next.
                    if response.status_code == 200:
                        
                        # "Verification" being in the request's response means it is available.
                        # Record an available license plate combination.
                        if "Verification" in str(response.content):
                            print(colored("PLATE AVAILABLE:  " + word, 'green'))
                            f = open("outputresults.txt", "a")
                            f.write(word + "\n")
                            f.close()

                        # "Verification" not being in the request's response means it is taken.
                        # Do not record a taken license plate combination.
                        else:
                            print(colored("PLATE UNAVAILABLE:  " + word, 'red'))
                        
                        # Exits the retry loop because a successful check was completed.
                        break

                    # Bad request, repeat it.
                    # Any bad request will trigger the exception below.

                # Increases the counter for total retries of checking the combination.
                except:
                    retries += 1


def generateCombinations(input_number):

    # Used for combination generation.
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"

    # Creating a list of all 1-character combinations.
    if input_number == 1:
        return [
            *[a for a in alphabet],
            *[b for b in alphabet]
        ]

    # Creating a list of all 3-character combinations.
    elif input_number == 2:
        return [
            *[a + b for a in alphabet for b in alphabet],
            *[a + b for a in alphabet for b in numbers],
            *[a + b for a in numbers for b in numbers]
        ]

    # Creating a list of all 3-letter combinations.
    elif input_number == 3:
        return [a + b + c for a in alphabet for b in alphabet for c in alphabet]

    # Creating a list of all 3-number combinations.
    elif input_number == 4:
        return [a + b + c for a in numbers for b in numbers for c in numbers]

    # Creating a list of all 3-letter words via GitHub scrape.
    elif input_number == 5:
        return requests.get(
            url="https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/WordLists/3letterwords.txt"
        ).text.split("\n")

    # Creating a list of all 4-letter words via GitHub scrape.
    elif input_number == 6:
        return requests.get(
            url="https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/WordLists/4letterwords.txt"
        ).text.split("\n")

    # Creating a list of all 5-letter words via GitHub scrape.
    elif input_number == 7:
        return requests.get(
            url="https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/WordLists/5letterwords.txt"
        ).text.split("\n")

    # Creating a list of all 6-letter words via GitHub scrape.
    elif input_number == 8:
        return requests.get(
            url="https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/WordLists/6letterwords.txt"
        ).text.split("\n")

    # Creating a list of all 3, 4, 5, 6 repeater combinations.
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

    # On-screen input for desired checks.
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

    # Holds the combinations to check.
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
