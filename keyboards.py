from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menue = InlineKeyboardMarkup(row_width=2)

back_to_menu = InlineKeyboardMarkup(inline_keyboard=[(
    InlineKeyboardButton(text='<< Личный кабинет', callback_data='back_to_profile'),
)], row_width=1)

main_buttons = [
    InlineKeyboardButton(text='🔍 Спарсить', callback_data='parse'),
    InlineKeyboardButton(text='📢 Канал прогера', url='https://t.me/+1A9f6ZFMJBgxMjRi')
]

# back_to_profile_referal = InlineKeyboardMarkup(inline_keyboard=[(
#     InlineKeyboardButton(text='<< Личный кабинет', callback_data='back_to_profile'),
# )], row_width=1)


main_menue.add(*main_buttons)
