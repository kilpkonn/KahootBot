"""Main."""
from colorama import init
from multiprocessing import Pool
import random

from log import Log
from bot import Bot


class Kahoot:
    """Kahoot."""

    def __init__(self):
        """Init."""
        log = Log("Root")
        log.info("Starting KahootBot...")
        self.game_pin = log.ask_input("Enter game PIN: ")
        self.bot_count = log.ask_input("Enter amount of bots to create:  ")
        p = Pool(self.bot_count)
        print(p.map(self.main, [x for x in range(self.bot_count)]))

    def main(self, name, number_of_questions=10):
        """Main."""
        bot = Bot(f"{name}", [random.choice(["red", "blue", "green", "yellow"]) for _ in range(number_of_questions)])
        bot.start(self.game_pin)


if __name__ == "__main__":
    init()
    Kahoot()
