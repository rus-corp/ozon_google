import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart


from data import bot_token


dp = Dispatcher()




@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
  await message.answer(f'Hello')




@dp.message()
async def message_handler(message: types.Message):
  pass


async def main():
  bot = Bot(token=bot_token)
  await dp.start_polling(bot)
  
  
if __name__ == '__main__':
  asyncio.run(main())