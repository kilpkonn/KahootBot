"""Configuration."""
import json
import random
from json import JSONDecodeError


class Configuration:
    """Configuration."""

    def __init__(self):
        """Init."""
        self.names = []
        self.names_given_out = []
        self.question_timeout = 60

    def get_name(self):
        """Get name for bot."""
        choices = [x for x in self.names if x not in self.names_given_out]
        if len(choices) <= 0:
            choices = [x + '_' for x in self.names]

        name_to_give = random.choice(choices)
        self.names_given_out.append(name_to_give)
        return name_to_give

    def load(self, file_name):
        """Load configuration."""
        try:
            with open(file_name, 'r', encoding="utf8") as f:
                data = json.load(f)
                self.question_timeout = data["question_timeout"]
            with open(data["path_to_names"], 'r', encoding="utf8") as names_file:
                names_data = json.load(names_file)
                self.names = names_data
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
                "path_to_names": "./names.json",
                "question_timeout": self.question_timeout,
                }, f)
