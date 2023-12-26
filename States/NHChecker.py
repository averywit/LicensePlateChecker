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
                    session.get(
                        url="https://business.nh.gov/Platecheck/platecheck.aspx",
                        timeout=10
                    )

                    data = {
                        "__LASTFOCUS": "",
                        "__VIEWSTATE": "/wEPDwUKMTEwMTE0OTU5Ng9kFgJmD2QWAgIBD2QWAgIBD2QWBAIBD2QWGAIJDxAPZBYCHghvbkNoYW5nZQUNQ2hhbmdlUGxhdGUoKWRkZAINDw8WAh4EVGV4dAUcU2VsZWN0IHBhc3NlbmdlciBwbGF0ZSB0eXBlOhYCHgVzdHlsZQUPZGlzcGxheTppbmxpbmU7ZAIPDxAPFgYeDURhdGFUZXh0RmllbGQFDVBsYXRlVHlwZVRleHQeDkRhdGFWYWx1ZUZpZWxkBQJJRB4LXyFEYXRhQm91bmRnFgQfAAURQ2hhbmdlUGFzc2VuZ2VyKCkfAgUPZGlzcGxheTppbmxpbmU7EBUPIS0tIFNlbGVjdCBQYXNzZW5nZXIgUGxhdGUgVHlwZSAtLShBbnRpcXVlIChpYW50aSkgICAgICAgICAgICAgICAgICAgICAgICAgKENvbnNlcnZhdGlvbiAoaWNwYXMgLSBNb29zZSBQbGF0ZSkgICAgICAoRGlzYWJsZWQgVmV0ZXJhbiAoaWR2ZXQpICAgICAgICAgICAgICAgIChGb3JtZXIgUE9XIChpZnBvdykgICAgICAgICAgICAgICAgICAgICAgKEhhbmRpY2FwcGVkIChpaGNhcCkgICAgICAgICAgICAgICAgICAgICAeSW5pdGlhbCBOYXRpb25hbCBHdWFyZCAoaW5nbmgpFUluaXRpYWwgUGFya3MgKGlzcHBzKSJJbml0aWFsIFBhcmtzIENvbnNlcnZhdGlvbiAoaXNwY3ApJEludGlpYWwgQWN0aXZlIER1dHkgTWlsaXRhcnkgKGlhZGFmKShQYXNzZW5nZXIgKGlwYXNzKSAgICAgICAgICAgICAgICAgICAgICAgKFBlYXJsIEhhcmJvciBTdXJ2aXZvciAoaXBoYnIpICAgICAgICAgICAoUHVycGxlIEhlYXJ0IChpbnB1cikgICAgICAgICAgICAgICAgICAgIChSZWd1bGFyIFZldGVyYW4gKGl2dmV0KSAgICAgICAgICAgICAgICAgKFN0cmVldCBSb2QgKGlzcm9kKSAgICAgICAgICAgICAgICAgICAgICAVDyEtLSBTZWxlY3QgUGFzc2VuZ2VyIFBsYXRlIFR5cGUgLS0FSUFOVEkFSUNQQVMFSURWRVQFSUZQT1cFSUhDQVAFSU5HTkgFSVNQUFMFSVNQQ1AFSUFEQUYFSVBBU1MFSVBIQlIFSU5QVVIFSVZWRVQFSVNST0QUKwMPZ2dnZ2dnZ2dnZ2dnZ2dnZGQCEQ8QDxYGHwMFDVBsYXRlVHlwZVRleHQfBAUCSUQfBWcWBB8ABRJDaGFuZ2VNb3RvcmN5Y2xlKCkfAgUNZGlzcGxheTpub25lOxAVBSEtLSBTZWxlY3QgUGFzc2VuZ2VyIFBsYXRlIFR5cGUgLS0oSGFuZGljYXAgTW90b3JjeWNsZSAoaWhtb3QpICAgICAgICAgICAgIChNb3RvcmN5Y2xlIChpbW90bykgICAgICAgICAgICAgICAgICAgICAgKFB1cnBsZSBIZWFydCBNb3RvcmN5Y2xlIChpcG1vdCkgICAgICAgICAoVmV0ZXJhbiBNb3RvcmN5Y2xlIChpdm1vdCkgICAgICAgICAgICAgIBUFIS0tIFNlbGVjdCBQYXNzZW5nZXIgUGxhdGUgVHlwZSAtLQVJSE1PVAVJTU9UTwVJUE1PVAVJVk1PVBQrAwVnZ2dnZ2RkAhMPEA8WBh8DBQ1QbGF0ZVR5cGVUZXh0HwQFAklEHwVnFgQfAAUSQ2hhbmdlQ29tbWVyY2lhbCgpHwIFDWRpc3BsYXk6bm9uZTsQFQMhLS0gU2VsZWN0IFBhc3NlbmdlciBQbGF0ZSBUeXBlIC0tKEFwcG9ydGlvbmVkIFZlaGljbGUgKGlhcHJvKSAgICAgICAgICAgICAoQ29tbWVyY2lhbCAoaWNvbW0pICAgICAgICAgICAgICAgICAgICAgIBUDIS0tIFNlbGVjdCBQYXNzZW5nZXIgUGxhdGUgVHlwZSAtLQVJQVBSTwVJQ09NTRQrAwNnZ2dkZAIVDxAPFgYfAwUNUGxhdGVUeXBlVGV4dB8EBQJJRB8FZxYEHwAFD0NoYW5nZVRyYWlsZXIoKR8CBQ1kaXNwbGF5Om5vbmU7EBUCIS0tIFNlbGVjdCBQYXNzZW5nZXIgUGxhdGUgVHlwZSAtLShUcmFpbGVyIChpdHJhaSkgICAgICAgICAgICAgICAgICAgICAgICAgFQIhLS0gU2VsZWN0IFBhc3NlbmdlciBQbGF0ZSBUeXBlIC0tBUlUUkFJFCsDAmdnZGQCFw8PZBYCHwIFDWRpc3BsYXk6bm9uZTtkAhkPDxYCHwEFFEVudGVyIHBsYXRlIHJlcXVlc3Q6FgIfAgUZZGlzcGxheTppbmxpbmU7Y29sb3I6cmVkO2QCGw8PFgIeCU1heExlbmd0aAIHFgIfAgUPZGlzcGxheTppbmxpbmU7ZAIdDw8WAh8BBRUoTWF4aW11bSBsZW5ndGggaXMgNykWAh8CBQ9kaXNwbGF5OmlubGluZTtkAh8PD2QWAh4Hb25DbGljawUTcmV0dXJuIFN1Ym1pdEZvcm0oKWQCIQ8PFgIfAQUVQ0FUIGlzIG5vdCBhdmFpbGFibGUhFgIfAgUPZGlzcGxheTppbmxpbmU7ZAICDw9kFgIfAgUNZGlzcGxheTpub25lOxYCAgUPDxYCHwEFBUlQQVNTZGRk/eQ2Fg+OlMt8Bz2cG7LZvKIwvSw=",
                        "__VIEWSTATEGENERATOR": "4F7B3EB8",
                        "__EVENTTARGET": "",
                        "__EVENTARGUMENT": "",
                        "__EVENTVALIDATION": "/wEWJwLh9ODFBgKQ1p+HDQL+6rbZCgLq6dOcCAKOn9WfDgK2hsSCCgLEr56yCAK74tHHBQK8x+4FAozz6LsBAuiNgOUBArbTxJEFAoaSm+4CAumK+twIAoqSt7sDAoSh/s8DAqCOle8OAoaSr8AOAouSs4QEAp3K97MJAtmX+uUNAq2kwosKAoWSn5MKAumKss4IAuWtv/0MAs/QxuYEAon3tZsKAriZsIsOAon31YMKAon3vYUKApGu6vMJAsuxpZIIAuTnwKUBAsnQosgBAtvwsYkOAtnfkvgOArrOvuIPApmB66YJAtWF/+0HMjFrEx1gdqOWEHMKWg87LVseBSM=",
                        "ctl00$cphMain$PlateTypeHiddenField": "PASS",
                        "ctl00$cphMain$SpecificTypeHiddenField": "IPASS",
                        "ctl00$cphMain$LengthHiddenField": "7",
                        "ctl00$cphMain$PlateField": "PASS",
                        "ctl00$cphMain$PassengerPlatesField": "IPASS",
                        "ctl00$cphMain$MotorcyclePlatesField": "-- Select Passenger Plate Type --",
                        "ctl00$cphMain$CommercialPlatesField": "-- Select Passenger Plate Type --",
                        "ctl00$cphMain$TrailerPlatesField": "-- Select Passenger Plate Type --",
                        "ctl00$cphMain$PlateRequestField": word,
                        "ctl00$cphMain$SubmitCommand": "Submit",
                        "ctl00$cphMain$JSTest": "1"
                    }
                    response = session.post(
                        url="https://business.nh.gov/Platecheck/platecheck.aspx",
                        data=data,
                        timeout=10
                    )

                    if response.status_code == 200:
                        if '<div id="ctl00_cphMain_ResultsDisplay" style="display:none;">' not in response.text:
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
