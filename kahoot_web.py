"""Kahoot web."""
import sys, time, json
import asyncio
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException

from log import Log


class KahootWeb:
    """Kahoot Web."""

    def __init__(self, log: Log):
        """Init."""
        self.log = log
        self.driver = None
        self.lookuptable = {'red': '.quiz-board > button:nth-of-type(1)',
                            'blue': '.quiz-board > button:nth-of-type(2)',
                            'yellow': '.quiz-board > button:nth-of-type(3)',
                            'green': '.quiz-board > button:nth-of-type(4)'}

    async def wait_for_item(self, driver, css, timeout=10):
        WebDriverWait(driver, timeout).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, css)))

    async def get_details(self, kahootid, email: str, password: str):
        authparams = {'username': email, 'password': password, 'grant_type': 'password'}
        self.log.info('Trying to authenticate')
        data = requests.post('https://create.kahoot.it/rest/authenticate',
                             data=json.dumps(authparams).encode(), headers={'content-type': 'application/json'}).json()
        if 'error' in data:
            self.log.error('Could not authenticate')
            exit()
        response = requests.get('https://create.kahoot.it/rest/kahoots/{}'.format(kahootid),
                                headers={'content-type': 'application/json',
                                         'authorization': data['access_token']}).json()
        if 'error' in response:
            self.log.error("Could not find kahoot ID (maybe it's private)")
            exit()
        qanda = {}
        color_sequence = []
        lookuptable = {0: 'red', 1: 'blue', 2: 'yellow', 3: 'green'}

        for question in response['questions']:
            for i in range(len(question['choices'])):
                if question['choices'][i]['correct']:
                    qanda[question['question']] = question['choices'][i]['answer']
                    color_sequence.append(lookuptable[i])
                    break
        print(qanda)
        return qanda, color_sequence

    async def connect(self, kahoot_id, name):
        """Connect to game."""
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.get('https://kahoot.it/#/')
        await self.wait_for_item(self.driver, '#inputSession')
        self.driver.find_element_by_css_selector('#inputSession').send_keys(kahoot_id)
        self.driver.find_element_by_css_selector('.btn-greyscale').click()
        await self.wait_for_item(self.driver, '#username')
        self.driver.find_element_by_css_selector('#username').send_keys(name)
        await asyncio.sleep(0.5)
        self.driver.find_element_by_css_selector('.btn-greyscale').click()
        self.log.success("Connected to Kahoot!")

    async def answer_question(self, answer):
        """Answer question."""
        try:
            self.driver.find_element_by_css_selector(self.lookuptable[answer]).click()
        except TimeoutException:
            self.log.error("Timed out answering question.")
        except ElementNotVisibleException:
            self.log.error("Question was skipped.")

    async def start_answering(self):
        """Start answering questions."""
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))

    async def wait_for_question(self, timeout: int = 60):
        """Wait for next question."""
        try:
            await self.wait_for_item(self.driver, "div#app", timeout=timeout)
        except TimeoutException:
            self.log.error("Timed out waiting for question.")

    async def quit(self):
        """Quit game."""
        self.driver.quit()
