from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
from data import get_wordle_answers
from solve import filter_answers, next_best_guesses

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

driver.get("https://www.nytimes.com/games/wordle/index.html")

sleep(0.5)

tracker_button_path = "//*[@id=\"pz-gdpr-btn-closex\"]"
try: # the tracker button may or may not be there
    close_tracker_button = driver.find_element(By.XPATH, tracker_button_path)
    close_tracker_button.click()
except:
    pass

sleep(0.25)

button_path = "/html/body/div/div/dialog/div/button"
close_button = driver.find_element(By.XPATH, button_path)
close_button.click()

sleep(0.25)

def getState(round):
    sleep(2.5)
    states = []
    for i in range(1, 6):
        xpath = "/html/body/div/div/div/div/div[1]/div/div[{round}]/div[{letter}]/div".format(round=round, letter=i)
        state = driver.find_element(By.XPATH, xpath).get_attribute("data-state")
        match state:
            case "absent":
                states.append(0)
            case "present":
                states.append(1)
            case "correct":
                states.append(2)
    return states

page = driver.find_element(By.CLASS_NAME, "pz-dont-touch")

guesses = get_wordle_answers()
answers = get_wordle_answers()
starting_guesses = "arise arose crate crane salet soare trace serai tales cones hates audio adieu dealt roate store stare pious ouija aisle ocean about"
starting_guesses = starting_guesses.split(" ")
guess = starting_guesses[random.randint(0, len(starting_guesses) - 1)]

for round in range(1,7):
    print("Round", round, flush=True)
    if len(answers) > 10:
        print("Number of possible answers left: ", len(answers), flush=True)
    else:
        print("Possible answers left: ", answers, flush=True)
    print("Guess: ", guess, flush=True)
    page.send_keys(guess)
    page.send_keys(Keys.ENTER)
    result = getState(round)
    print("Result: ", result, flush=True)
    if result == [2,2,2,2,2]:
        print()
        print("Solved!")
        break
    answers = filter_answers(guess, result, answers)
    best_guesses = next_best_guesses(guesses, answers)
    if len(best_guesses) == 1:
        print("Best guess for next round: ", best_guesses[0], flush=True)
        guess = best_guesses[0]
    else:
        print("Best guesses for next round: ", best_guesses, flush=True)
        guess = best_guesses[random.randint(0, len(best_guesses) - 1)]
    print()

sleep(3)

button_path = "/html/body/div/div/dialog/div/button"
button = driver.find_element(By.XPATH, button_path)
button.click()
