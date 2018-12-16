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

    def start(self, pin):
        """Start Bot."""
        self.log.info(f"Starting bot {self.name}...")
        self.kahoot_web.connect(pin, self.name)
        self.log.success("Connected to game!")
        self.kahoot_web.start_answering()
        for i in range(len(self.color_sequence)):
            if i == 0:
                self.kahoot_web.wait_for_question(timeout=360)
            else:
                self.kahoot_web.wait_for_question(timeout=self.question_timeout)
            self.log.info("Answering question")
            self.kahoot_web.answer_question(self.color_sequence[i])
        self.log.success("Done quiz!")

