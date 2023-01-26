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

            req.get(url="https://business.nh.gov/Platecheck/platecheck.aspx")

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
            response = req.post(url="https://business.nh.gov/Platecheck/platecheck.aspx", data=data)

            if '<div id="ctl00_cphMain_ResultsDisplay" style="display:none;">' not in response.text:
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
