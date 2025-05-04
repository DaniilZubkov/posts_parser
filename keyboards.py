from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# main_menue = InlineKeyboardMarkup(row_width=2)


def main_menue():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='🔍 Спарсить', callback_data='parse'),
        InlineKeyboardButton(text='📢 Канал прогера', url='https://t.me/+1A9f6ZFMJBgxMjRi')
    )
    builder.adjust(1)
    return builder.as_markup()


# back_to_menu = InlineKeyboardMarkup(inline_keyboard=[(
#     InlineKeyboardButton(text='<< Личный кабинет', callback_data='back_to_profile'),
# )], row_width=1)



def back_to_menu():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='<< Личный кабинет', callback_data='back_to_profile'),
    )
    return builder.as_markup()


# main_buttons = [
#     InlineKeyboardButton(text='🔍 Спарсить', callback_data='parse'),
#     InlineKeyboardButton(text='📢 Канал прогера', url='https://t.me/+1A9f6ZFMJBgxMjRi')
# ]


# main_menue.add(*main_buttons)
