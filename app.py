from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import slack
import os
from pathlib import Path
from dotenv import load_dotenv
import json
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
display.start()

with open('./lastTest.json') as f:
  lastTestJSON = json.load(f)

lastTest = lastTestJSON.get('lastTest')
print(lastTest)

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=options)

wait = WebDriverWait(driver, 100)

try:
    driver.get("https://ouders.sgsintpaulus.be/")
    print("gelukt1")

    #login
    time.sleep(5)
    elementUsername = wait.until(EC.presence_of_element_located((By.ID, "login-user-inputEl")))
    elementPassword = wait.until(EC.presence_of_element_located((By.ID, "login-password-inputEl")))
    print("gelukt2")

    elementUsername.send_keys("peter.n@telenet.be")
    elementPassword.send_keys("22320")
    elementPassword.send_keys(Keys.RETURN)
    print("gelukt3")

    time.sleep(10)
    elementPlusje = wait.until(EC.presence_of_element_located((By.ID, 'lltree25759')))
    print("gelukt4.1")
    elementPlusje.click()
    print("gelukt4.2")

    time.sleep(10)
    elementRapport = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'llrapport')))
    elementRapport.click()
    print("gelukt5")

    time.sleep(10)
    elementRapportBtn = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/em/button/span[1]')))
    elementRapportBtn.click()
    print("gelukt6")

    time.sleep(10)
    driver.get("https://online.myro.be/logbook.php?Recent")
    table_id = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'studentBody')))
    rows = table_id.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table

    for row in rows:
        colVak = row.find_elements(By.TAG_NAME, "td")[0]
        colTitle = row.find_elements(By.TAG_NAME, "td")[1]
        colPoint = row.find_elements(By.TAG_NAME, "td")[2]
        colMax = row.find_elements(By.TAG_NAME, "td")[3]

        print("lastTest: " + colVak.text + " " + colTitle.text + " Punten: " + colPoint.text + colMax.text) #prints text from the element

        if lastTest == colTitle.text:
            print("No change")
        else: 
            lastTest = colTitle.text
            lastTestJSON['lastTest'] = colTitle.text

            with open('./lastTest.json', 'w') as json_file:
                json.dump(lastTestJSON, json_file)

            #slack notification 
            client.chat_postMessage(channel='#punten', text= "Nieuwe punten: " + colVak.text + " " + colTitle.text + ": Punten: " + colPoint.text + colMax.text)

        break

    driver.quit()

except:
    print("Error")
    #client.chat_postMessage(channel='#punten', text= "Kan geen punten laden")
    driver.quit()
