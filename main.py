import asyncio
import json
import os
import subprocess

from aiogram.types import FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from keyboards import main_menue, back_to_menu
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, F, types



bot = Bot('7715234303:AAGBPPezu6HbdbRsO-GJ14gvuOjKBLOPfPo')
dp = Dispatcher(storage=MemoryStorage())



class Q_classes(StatesGroup):
    q1 = State()



# СОБИРАЕМ ПОСТЫ...
def collect_posts(channel):
    with open(f"{channel}.txt") as file:
        file = file.readlines()

    posts = []
    for n, line in enumerate(file):
        file[n] = json.loads(file[n])
        links = [link for link in file[n]['outlinks'] if channel not in link]
        p = str(file[n]['content']) + "\n\n" + str("\n".join(links))
        posts.append(p)

    return posts




# ВЫКЛАДЫВАЕМ ПОСТЫ
def upload_posts(num_posts, channel):
    command = f'snscrape --max-result {num_posts} --jsonl telegram-channel {channel} > {channel}.txt'
    subprocess.run(command, shell=True)




@dp.message(Command('start'))
async def start_command(message: Message):
    photo_path = 'fotos/black.jpg'
    await message.answer_photo(photo=FSInputFile(photo_path), caption=f"👨🏻‍💻 <b>Привет, {message.from_user.first_name}! Это бот, который спарсит посты групп, чатов, каналов и отправляет в твой канал</b>\n\n"
                                                                     f"Выберите действие:", reply_markup=main_menue(), parse_mode='html')

@dp.callback_query(lambda F: True)
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    query = callback_query.data
    molny_photo_path = 'fotos/lightning.jpg'
    photo_path = 'fotos/black.jpg'

    if query == 'parse':
        await state.set_state(Q_classes.q1)
        await callback_query.message.answer_photo(photo=FSInputFile(molny_photo_path), caption='***1.*** Введите название чата, который вы хотите спарсить\n\n'
                                                                                              '***2.*** Введите количество постов \n\n'
                                                                                              '***3.*** Введите свой канал куда будут выкладываться посты:\n\n'
                                                                                              '***Пример:*** `another_channel 10 your_cahnnel`', reply_markup=back_to_menu(), parse_mode='MARKDOWN')

    if query == 'back_to_profile':
        await callback_query.message.answer_photo(photo=FSInputFile(photo_path),
                                   caption=f"👨🏻‍💻 <b>Привет, {callback_query.from_user.first_name}! Это бот, который спарсит посты групп, чатов, каналов и отправляет в твой канал</b>\n\n"
                                           f"Выберите действие:", reply_markup=main_menue(), parse_mode='html')



@dp.callback_query(Q_classes.q1)
async def back_to_profile_interval(callback_query: CallbackQuery, state: FSMContext):
    success_photo_path = 'fotos/success.jpg'
    await state.clear()
    await callback_query.message.answer_photo(photo=FSInputFile(success_photo_path), caption='✅❌ <b>Ввод отменен...</b>\n\n'
                                                                                 '<i>Нажмите любую кнопку чтобы продолжить</i>', parse_mode='html', reply_markup=back_to_menu())
    return



@dp.message(Q_classes.q1)
async def get_chat_name(message: Message, state: FSMContext):
    error_photo = 'fotos/error.jpg'
    success_photo_path = 'fotos/success.jpg'

    try:
        channel, num, target_channel = str(message.text).split()
        target_channel = '@'+target_channel

        upload_posts(num, channel)
        posts = collect_posts(channel)

        while posts:
            await bot.send_message(target_channel, posts.pop())
        await message.answer_photo(photo=FSInputFile(success_photo_path), caption=f'<b>Пересылка с @{channel} завершена успешно!</b>', parse_mode='html', reply_markup=back_to_menu())
        await state.clear()

        os.remove(f'{channel}.txt')

    except Exception:
        await message.answer_photo(photo=FSInputFile(error_photo), caption='***Ошибка...***', parse_mode='MARKDOWN', reply_markup=back_to_menu())
        await state.set_state(Q_classes.q1)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
