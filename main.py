"""Main."""
from colorama import init
import asyncio

from kahoot_manager import KahootManager


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
