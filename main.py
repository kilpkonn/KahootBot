"""Main."""
from colorama import init

from kahoot_manager import KahootManager


def main():
    """Main."""
    manager_thread = KahootManager()
    manager_thread.start()
    while True:
        data = input()
        manager_thread.input_queue.put(data)
        if data.lower() == "exit":
            break
    manager_thread.join()


if __name__ == "__main__":
    init()
    main()
