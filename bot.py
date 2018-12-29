"""Bot."""
from kahoot_web import KahootWeb
from log import Log


class Bot:
    """Bot."""

    def __init__(self, name: str, color_sequence, question_timeout: int = 60):
        """Init."""
        self.name = name
        self.log = Log(self.name)
        self.color_sequence = color_sequence
        self.question_timeout = question_timeout
        self.kahoot_web = KahootWeb(self.log)
        self.question = 0

    async def start(self, pin):
        """Start Bot."""
        self.log.info(f"Starting bot {self.name}...")
        await self.kahoot_web.connect(pin, self.name)
        self.log.success("Connected to game!")
        await self.kahoot_web.start_answering()
        self.question = 0

    async def wait_for_question(self):
        """Wait for question."""
        await self.kahoot_web.wait_for_question(timeout=360)

    async def answer_question(self):
        """Answer question."""
        self.log.info("Answering question")
        await self.kahoot_web.answer_question(self.color_sequence[self.question])
        self.question += 1
        self.log.success("Done quiz!")

    async def stop(self):
        """Stop bot."""
        self.log.info("Stopping bot!")
        await self.kahoot_web.quit()
