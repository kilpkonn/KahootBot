"""Main."""
from colorama import init

from log import Log
from bot import Bot


def main():
    """Main."""
    init()
    log = Log("Root")
    log.info("Starting KahootBot...")
    log.info("Enter game PIN!")
    game_pin = input("PIN: ")
    bot = Bot(f"Test", ["red" for _ in range(10)])
    bot.start(game_pin)


if __name__ == "__main__":
    main()
