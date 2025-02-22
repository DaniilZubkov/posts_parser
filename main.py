import json
import subprocess

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher, Bot
from aiogram import executor
from keyboards import main_menue, back_to_menu
from aiogram.dispatcher import FSMContext


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


class Q_classes(StatesGroup):
    q1 = State()


bot = Bot(token='7783210062:AAFC_H7lRdIPdcSrdbII_ETa0PY1pcTM25M')
dp = Dispatcher(bot, storage=MemoryStorage())



@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    photo_path = 'fotos/black.jpg'
    await message.answer_photo(photo=open(photo_path, "rb"), caption=f"👨🏻‍💻 <b>Привет, {message.from_user.first_name}! Это бот, который спарсит посты групп, чатов, каналов и отправляет в твой канал</b>\n\n"
                                                                     f"Выберите действие:", reply_markup=main_menue, parse_mode='html')

@dp.callback_query_handler(lambda CallbackQuery: True)
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    query = callback_query.data
    if query == 'parse':
        molny_photo_path = 'fotos/lightning.jpg'
        await state.set_state(Q_classes.q1)
        await callback_query.message.answer_photo(photo=open(molny_photo_path, "rb"), caption='***1.*** Введите название чата, который вы хотите спарсить\n\n'
                                                                                              '***2.*** Введите количество постов \n\n'
                                                                                              '***3.*** Введите свой канал куда будут выкладываться посты:\n\n'
                                                                                              '***Пример:*** `another_channel 10 your_cahnnel`', reply_markup=back_to_menu, parse_mode='MARKDOWN')


@dp.message_handler(state=Q_classes.q1)
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
        await message.answer_photo(photo=open(success_photo_path, "rb"), caption=f'<b>Пересылка с {channel} завершена успешно!</b>', parse_mode='html')
        await state.finish()

    except Exception:
        await message.answer_photo(photo=open(error_photo, "rb"), caption='***Ошибка...***\n\n'
                                                                          'Пожалуйста введите правильные данные', parse_mode='MARKDOWN')
        await state.reset_state()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
