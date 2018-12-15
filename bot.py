"""Bot."""
from kahoot_web import KahootWeb
from log import Log


class Bot:
    """Bot."""

    def __init__(self, name: str, color_sequence):
        """Init."""
        self.name = name
        self.log = Log(self.name)
        self.color_sequence = color_sequence
        self.kahoot_web = KahootWeb(self.log)

    def start(self, pin):
        """Start Bot."""
        self.log.info(f"Starting bot {self.name}...")
        self.kahoot_web.connect(pin, self.name)
        self.log.success("Connected to game!")
        self.kahoot_web.start_answering()
        for i in range(len(self.color_sequence)):
            self.kahoot_web.wait_for_question()
            self.log.info("Answering question")
            self.kahoot_web.answer_question("red")
        self.log.success("Done quiz!")

