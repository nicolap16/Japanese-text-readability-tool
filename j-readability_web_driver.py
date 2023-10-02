import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from corpus import N4_test # This is a test text in the corpus that should be N5 level

# Web driver tool modified from https://www.youtube.com/watch?v=EELySnTPeyw. Accessed on 19th July 2023. 

def jreadability_result(text):
    url = "https://jreadability.net/sys/en"
    browser = webdriver.Firefox()
    browser.get(url)

    press = browser.find_element(By.ID,'terms_of_use_button')
    ActionChains(browser).click(press).perform()
    print("CLICKED")
    browser.implicitly_wait(6)

    search_box = browser.find_element(By.ID,"text")
    search_box.send_keys(text)
    print("TYPED")

    run = browser.find_element(By.ID, "execute")
    ActionChains(browser).click(run).perform()
    browser.implicitly_wait(5)
    print(f"SEARCHED for {text} \n")


    readLevel = browser.find_element(By.ID, "guideline").text
    print(f"This text you entered is {readLevel} \n")
    score = browser.find_element(By.ID,"score").text
    print(f"with a readability score of: {score} \n")

    browser.close()

# Test the tool with what should be an N5 text:
jreadability_result(N4_test)

