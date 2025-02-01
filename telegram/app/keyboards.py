from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="")],
                                     [KeyboardButton(text="Help")]], resize_keyboard=True, input_field_placeholder="Выберете пункт")