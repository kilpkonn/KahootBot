"""Main."""
from colorama import init, Fore

from kahoot_manager import KahootManager


def print_help():
    """Print help."""
    print(f"""{Fore.LIGHTCYAN_EX}Commands:
    {Fore.MAGENTA}help {Fore.GREEN} -> {Fore.WHITE}Print help to console.
    {Fore.MAGENTA}restart {Fore.GREEN} -> {Fore.YELLOW}Restart bots. [not implemented]
    {Fore.MAGENTA}exit {Fore.GREEN}-> {Fore.RED}Exit program!""")


def main():
    """Main."""
    manager_thread = KahootManager()
    manager_thread.start()
    while True:
        data = input()
        if data.lower() == "exit":
            manager_thread.input_queue.put(data)
            break
        elif data.lower() == "help":
            print_help()
        else:
            manager_thread.input_queue.put(data)

    manager_thread.join()


if __name__ == "__main__":
    init()
    main()
