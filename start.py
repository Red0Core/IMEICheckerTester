import backend.main
import tg_bot.main
from logger import logger
import asyncio
import platform
import uvicorn

async def main():
    config = uvicorn.Config(backend.main.app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)

    await asyncio.gather(
        asyncio.create_task(tg_bot.main.main()),
        asyncio.create_task(server.serve())
    )

if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        logger.info("Используется WindowsSelectorEventLoopPolicy для Windows.")
        asyncio.run(main())
    elif platform.system() == "Linux":
        try:
            import uvloop
            logger.info("Используется uvloop для Linux.")
            uvloop.run(main())
        except ImportError:
            logger.warning("uvloop не установлен, используется стандартный asyncio.")
    else:
        logger.info("Используется стандартный asyncio.")
        asyncio.run(main())
