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
                    session = requests.Session()

                    # Headers to complete the combination check.
                    headers = {
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

                    # Data to complete the combination check.
                    data = {
                        "txtLicense1": "",
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

                    # Reformats the data to fit the schema for checking the combination
                    for character in range(len(word)):
                        data[f"txtLicense{character + 1}"] = f"{word[character]}"

                    # Make the request to complete the combination check.
                    # Timeout of 10 seconds incase of a stuck request.
                    response = session.post(
                        url="https://www12.honolulu.gov/specialplates/main/frmInquiry.asp?sFlag=search&sType=",
                        headers=headers,
                        data=data,
                        timeout=10
                    )

                    # Successful request, continue to the next.
                    if response.status_code == 200:

                        # "class="text-msg-blue">Congratulations!" being in the request's response means it is available.
                        # Record an available license plate combination.
                        if 'class="text-msg-blue">Congratulations!' not in str(response.text):
                            print(colored("PLATE UNAVAILABLE:  " + word, 'red'))

                        # "class="text-msg-blue">Congratulations!" not being in the request's response means it is taken.
                        # Do not record a taken license plate combination.
                        else:
                            print(colored("PLATE AVAILABLE:  " + word, 'green'))
                            f = open("outputresults.txt", "a")
                            f.write(word + "\n")
                            f.close()

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
