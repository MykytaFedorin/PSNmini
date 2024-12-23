import asyncio

async def start_web_app():
    from frontend import app
    import uvicorn
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()

async def start_bot():
    from handlers import form_router
    from loader import bot, dp
    dp.include_router(form_router)
    await dp.start_polling(bot)

async def main() -> None:
    await asyncio.gather(
        start_web_app(),
        start_bot(),
    )

if __name__ == "__main__":
    asyncio.run(main())

