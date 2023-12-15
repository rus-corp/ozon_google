import json
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
import pyuseragents
import aiohttp

from data import bot_token


bot = Bot(token=bot_token)


dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
  user_id = message.from_user.id
  print(user_id)
  await message.answer('Введите пароль:')


@dp.message(F.text == 'ozon')
async def message_handler(message: types.Message):
  await message.answer('password correct')
  user_id = message.from_user.id
  with open('users.txt', 'a+') as file:
    file.write(str(user_id) + '\n')



async def bot_send_message(bot: Bot, text):
  with open('users.txt') as file:
    users = file.readlines()
  for user in users:
    user_id = user.strip()
    await bot.send_message(chat_id=user_id, text=text)



@dp.message(F.text)
async def second_message_handler(message: types.Message):
  await message.answer('Мои возможности ограничены, введите пароль')


async def telegram_notify(message, token, chat_id):
    """
    Отправляет уведомления в телеграм
    :param message:
    :param token:
    :param chat_id:
    :return:
    """
    try:
        url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}'
        headers = {
            'user-agent': pyuseragents.random()
        }
        async with aiohttp.ClientSession( trust_env=True) as session:
            async with session.get(url, headers=headers) as response:
                pass
    except:
        print('Не пошло уведомление')




async def telegram_main():
  await dp.start_polling(bot)
  

  
def run_bot():
  asyncio.run(telegram_main())