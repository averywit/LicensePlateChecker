from selenium import webdriver
import requests
import time

from termcolor import colored
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

serv = Service("/Users/avery/Downloads/chromedriver")
chrome_options = Options()
driver = webdriver.Chrome(service=serv, options=chrome_options)

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

driver.get("http://www.dmv.penndot.gov/vehicle_services/vrvanity.jsp?navigation=true")
time.sleep(2)
driver.find_element(By.XPATH, "/html/body/div/form[2]/table/tbody/tr[7]/td[1]/input").click()
time.sleep(2)
driver.find_element(By.NAME, "continueButton").click()
time.sleep(2)
driver.find_element(By.XPATH, "/html/body/div/table[2]/tbody/tr/td/a[5]").click()
time.sleep(2)

for i in lines:
    driver.find_element(By.XPATH, "/html/body/div/form[2]/table/tbody/tr[1]/td/table/tbody/tr[2]/td/input[1]").send_keys(i)
    driver.find_element(By.XPATH, "/html/body/div/form[2]/table/tbody/tr[1]/td/table/tbody/tr[3]/td/input[1]").click()
    if '<div id="A" style="color:#33CC00;display:none">  <strong>Plate configuration requested is available.</strong> </div>' not in driver.page_source:
        print(colored("PLATE AVAILABLE:  " + i, 'green'))
        f = open("outputresults.txt", "a")
        f.write(i + "\n")
        f.close()
    else:
        print(colored("PLATE UNAVAILABLE:  " + i, 'red'))
    driver.find_element(By.XPATH, "/html/body/div/form[2]/table/tbody/tr[1]/td/table/tbody/tr[3]/td/input[2]").click()
