"""Main."""
from colorama import init
import asyncio
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
        self.number_of_questions = None
        self.config = None
        self.bots = []

    async def load_configuration(self):
        """Boot KahootBot."""
        self.config = Configuration()
        self.config.load("./configuration/config.json")

    async def play(self):
        """Play game"""
        if not self.game_pin or self.game_pin == 0:
            self.game_pin = self.log.ask_input("Enter game PIN: ")
        if not self.bot_count or self.bot_count == 0:
            self.bot_count = int(self.log.ask_input("Enter amount of bots to create: "))
        if not self.number_of_questions or self.number_of_questions == 0:
            self.number_of_questions = int(self.log.ask_input("Enter the amount of questions: "))
        tasks = []
        for i in range(self.bot_count):
            bot = Bot(f"{self.config.get_name()}",
                      [random.choice(["red", "blue", "green", "yellow"]) for _ in range(self.number_of_questions)],
                      question_timeout=self.config.question_timeout)
            tasks.append(bot.start(self.game_pin))
            self.bots.append(bot)
            if i % 5 == 4:
                await asyncio.wait(tasks)
                tasks = []

        for _ in range(self.number_of_questions):
            await self.bots[0].wait_for_question()
            await asyncio.wait([x.answer_question() for x in self.bots])

        await asyncio.wait([x.stop() for x in self.bots])
        self.log.success("Done quiz!")


async def main():
    """Main."""
    kahoot_manager = KahootManager()
    await kahoot_manager.load_configuration()
    await kahoot_manager.play()


if __name__ == "__main__":
    init()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(main())
