"""Main."""
from colorama import init
import asyncio

from log import Log
from bot import Bot
from kahoot_web import KahootWeb
from configuration import Configuration


class KahootManager:
    """KahootManager."""

    def __init__(self):
        """Init."""
        self.log = Log("Root")
        self.log.info("Starting KahootBot...")
        self.kahoot_web = KahootWeb(self.log)
        self.input = ''
        self.game_details = None
        self.game_pin = None
        self.bot_count = None
        self.bot_pool = None
        self.kahoot_id = None
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
        if not self.kahoot_id or self.kahoot_id == '':
            self.kahoot_id = str(self.log.ask_input("Enter the ID of Kahoot!: "))
            if not self.kahoot_id or self.kahoot_id == '':
                self.game_details = (None, None)
            else:
                self.game_details = await self.kahoot_web.get_details(self.kahoot_id)

        tasks = []
        for i in range(self.bot_count):
            bot = Bot(f"{self.config.get_name()}",
                      self.game_details[1],
                      question_timeout=self.config.question_timeout)
            tasks.append(bot.start(self.game_pin))
            self.bots.append(bot)
            if i % 5 == 4:
                await asyncio.wait(tasks)
                tasks = []
        if tasks:
            await asyncio.wait(tasks)
        n = 0
        self.input = self.log.ask_input("Enter exit to stop!")
        while n > 0 or self.input.lower() != "exit":
            if self.input.isdigit():
                n = int(self.input)

            await self.bots[0].wait_for_question()
            tasks = []
            for i, bot in enumerate(self.bots):
                tasks.append(bot.answer_question())
                if i % 5 == 4:
                    await asyncio.wait(tasks)
                    tasks = []
            if tasks:
                await asyncio.wait(tasks)
            if n == 0:
                self.input = self.log.ask_input("Enter exit to stop!")
            else:
                n -= 1

        self.log.info("Stopping bots!")
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
