from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

class ComandKeyboard:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    def __init__(self,one_time,*args) -> None:
        self.kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
        for b in args:
            self.kb.add(b)

kbc = ComandKeyboard(True,'/register', '/start') 
kbr = ComandKeyboard(False,'/register')   