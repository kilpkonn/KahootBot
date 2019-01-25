"""Kahoot Manager."""
import asyncio
import queue
import threading

from log import Log
from bot import Bot
from kahoot_web import KahootWeb
from configuration import Configuration


class KahootManager(threading.Thread):
    """KahootManager."""

    def __init__(self):
        """Init."""
        super(KahootManager, self).__init__()
        self._stop_event = threading.Event()

        self.log = Log("Root")
        self.log.info("Starting KahootBot...")
        self.kahoot_web = KahootWeb(self.log)
        self.input_queue = queue.Queue()
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

    def run(self):
        """Play game."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.main())

    async def main(self):
        """Main function in KahootManager."""
        await self.load_configuration()
        await self.play()

    async def play(self):
        """Play game."""
        if not self.game_pin or self.game_pin == 0:
            self.log.ask_input("Enter game PIN: ")
            self.game_pin = str(await self._wait_for_input())
        if not self.bot_count or self.bot_count == 0:
            self.log.ask_input("Enter amount of bots to create: ")
            self.bot_count = int(await self._wait_for_input())
        if not self.kahoot_id or self.kahoot_id == '':
            self.log.ask_input("Enter the ID of Kahoot!: ")
            self.kahoot_id = str(await self._wait_for_input(accept_blank=True))
            if not self.kahoot_id or self.kahoot_id.strip() == '':
                self.game_details = (None, None)
            else:
                self.game_details = await self.kahoot_web.get_details(self.kahoot_id)

        for i in range(self.bot_count):
            bot = Bot(f"{self.config.get_name()}",
                      self.game_details[1],
                      question_timeout=self.config.question_timeout)
            self.bots.append(bot)

        await self.start_bots()
        self.log.ask_input("Enter 'exit' to stop!")
        while self.bots and not self.stopped():
            await self._wait_for_input(accept_blank=True)
            await self.bots[0].wait_for_question()
            tasks = []
            for i, bot in enumerate(self.bots):
                if not bot.running:
                    self.bots.remove(bot)
                    continue

                tasks.append(bot.answer_question())
                if i % 5 == 4:
                    await asyncio.wait(tasks)
                    tasks = []
            if tasks:
                await asyncio.wait(tasks)

        await self.stop_bots()
        self.log.success("Done quiz!")

    async def start_bots(self):
        """Start bots."""
        tasks = []
        for i, bot in enumerate(self.bots):
            tasks.append(bot.start(self.game_pin))
            if i % 5 == 4:
                await asyncio.wait(tasks)
                tasks = []
        if tasks:
            await asyncio.wait(tasks)

    async def stop_bots(self):
        """Stop bots."""
        if not self.bots:
            return
        self.log.info("Stopping bots!")
        await asyncio.wait([x.stop() for x in self.bots])

    async def check_for_command(self, input_str):
        """Check if input is command and handle it."""
        if input_str == "exit":
            await self.stop_bots()
        elif input_str == "restart":
            pass
        else:
            return input_str

    def stop(self):
        """Stop thread."""
        self._stop_event.set()

    def stopped(self):
        """Check if thread is stopped."""
        return self._stop_event.is_set()

    async def _wait_for_input(self, accept_blank: bool = False):
        """Wait for input."""
        while True:
            await asyncio.sleep(0.05)
            if not self.input_queue.empty():
                data = self.input_queue.get()
                if await self.check_for_command(data) and (accept_blank or data != ""):
                    break
            elif accept_blank:
                return ''
        return data
