"""Configuration."""
import json
from json import JSONDecodeError


class Configuration:
    """Configuration."""

    def __init__(self):
        """Init."""
        self.names = []
        self.question_timeout = 60

    def load(self, file_name):
        """Load configuration."""
        try:
            with open(file_name, 'r') as f:
                data = json.load(f)
                self.names = data["names"]
                self.question_timeout = data["question_timeout"]
            return data
        except JSONDecodeError:
            print("Specified config file is corrupt. Choose if you want to overwrite it!")
            choise = input("[Y/N]: ")
            if choise.lower() == 'y':
                print("Overwriting...")
                self.save(file_name)
            else:
                print("Using default configuration.")
                return self

        except FileNotFoundError:
            print("Specified config file doesn't exist!")
            print("Generating new config file.")
            self.save(file_name)

    def save(self, file_name):
        """Save configuration."""
        with open(file_name, 'w') as f:
            json.dump({
                "names": self.names,
                "question_timeout": self.question_timeout,
                }, f)
