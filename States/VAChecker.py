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
                session = requests.session()

                session.get(url="https://www.dmv.virginia.gov/dmvnet/plate_purchase/select_plate.asp?PLTNO=")

                data = {
                    "TransType": "INQ",
                    "TransID": "RESINQ",
                    "ReturnPage": "/dmvnet/plate_purchase/s2end.asp",
                    "HelpPage": "",
                    "Choice": "A",
                    "PltNo": f"{word}",
                    "HoldISA": "N",
                    "HoldSavePltNo": "",
                    "HoldCallHost": "",
                    "NumCharsInt": "8",
                    "CurrentTrans": "plate_purchase_reserve",
                    "PltType": "IGWT",
                    "PltNoAvail": "",
                    "PersonalMsg": "Y",
                    "Let1": f"{word[0]}",
                    "Let2": f"{word[1]}",
                    "Let3": f"{word[2]}",
                    "Let4": f"{word[3]}",
                    "Let5": f"{word[4]}",
                    "Let6": f"{word[5]}",
                    "Let7": f"{word[6]}",
                    "Let8": f"{word[7]}"
                }
                response = session.post(url="https://www.dmv.virginia.gov/dmvnet/common/router.asp", data=data)

                if "Congratulations" in response.text:
                    print(colored("PLATE AVAILABLE:  " + word, 'green'))
                    f = open("outputresults.txt", "a")
                    f.write(word.strip() + "\n")
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
            lines.insert(index, i + "       ")
            index += 1
        for i in numbers:
            lines.insert(index, i + "       ")
            index += 1
    # Creating an array of all 2 letter combinations
    if choice == 2:
        for i in alphabet:
            for j in alphabet:
                lines.insert(index, i + j + "      ")
                index += 1
            for k in numbers:
                lines.insert(index, i + k + "      ")
                index += 1
        for l in numbers:
            for m in numbers:
                lines.insert(index, l + m + "      ")
                index += 1
            for n in alphabet:
                lines.insert(index, l + n + "      ")
    # Creating an array of all 3 letter combinations
    elif choice == 3:
        for i in alphabet:
            for j in alphabet:
                for k in alphabet:
                    lines.insert(index, i + j + k + "     ")
                    index += 1
    # Retrieving the list of all 3 letter words from Github scrape
    elif choice == 4:
        url = "https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/3letterwords.txt"
        r = requests.get(url)
        for line in r.iter_lines():
            if line:
                lines.insert(index, str(line).strip("b'") + "     ")
                index += 1
    # Retrieving the list of all 4 letter words from Github scrape
    elif choice == 5:
        url = "https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/4letterwords.txt"
        r = requests.get(url)
        for line in r.iter_lines():
            if line:
                stupidparse = str(line)
                lines.insert(index, stupidparse[2:6] + "    ")
                index += 1

    # Retrieving the list of all 5 letter words from Github scrape
    elif choice == 6:
        url = "https://raw.githubusercontent.com/averywit/LicensePlateChecker/main/5letterwords.txt"
        r = requests.get(url)
        for line in r.iter_lines():
            if line:
                stupidparse = str(line)
                lines.insert(index, stupidparse[2:7] + "   ")
                index += 1

    # Creating an array of all 3 number combinations
    elif choice == 7:
        for i in numbers:
            for j in numbers:
                for k in numbers:
                    lines.insert(index, i + j + k + "     ")
                    index += 1

    # Creating an array of all 3 letter repeater combinations
    elif choice == 8:
        for i in alphabet:
            lines.insert(index, i + i + i + "     ")
            index += 1
        for j in alphabet:
            lines.insert(index, j + j + j + j + "    ")
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
