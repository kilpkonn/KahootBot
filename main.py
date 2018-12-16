"""Main."""
from colorama import init
from multiprocessing import Pool
import random

from log import Log
from bot import Bot
from configuration import Configuration


class KahootManager:
    """KahootManager."""

    def __init__(self):
        """Init."""
        self.log = Log("Root")
        self.log.info("Starting KahootBot...")
        self.game_pin = None
        self.bot_count = None
        self.bot_pool = None
        self.config = None

    def load_configuration(self):
        """Boot KahootBot."""
        self.config = Configuration()
        self.config.load("./configuration/config.json")

    def play(self):
        """Play game"""
        if not self.game_pin or self.game_pin == 0:
            self.game_pin = self.log.ask_input("Enter game PIN: ")
        if not self.bot_count or self.bot_count == 0:
            self.bot_count = int(self.log.ask_input("Enter amount of bots to create: "))

        p = Pool(self.bot_count)
        p.map(self.main, [self.config.get_name() for _ in range(self.bot_count)])

    def main(self, name, number_of_questions=10):
        """Main."""
        bot = Bot(f"{name}",
                  [random.choice(["red", "blue", "green", "yellow"]) for _ in range(number_of_questions)],
                  question_timeout=self.config.question_timeout)
        bot.start(self.game_pin)


if __name__ == "__main__":
    init()
    kahoot_manager = KahootManager()
    kahoot_manager.load_configuration()
    kahoot_manager.play()
