"""Main."""
from colorama import init
import asyncio
import threading

from kahoot_manager import KahootManager


async def main():
    """Main."""
    kahoot_manager = KahootManager()
    await kahoot_manager.load_configuration()
    manager_thread = threading.Thread(target=kahoot_manager.run)
    manager_thread.start()
    while True:
        await asyncio.sleep(0.05)
        data = input()
        kahoot_manager.input_queue.put(data)
        if data.lower() == "exit":
            break
    manager_thread.join()

if __name__ == "__main__":
    init()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(main())
