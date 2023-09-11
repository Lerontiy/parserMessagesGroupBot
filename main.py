import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from settings import get_token, get_password
from database import db
from messages import answerMessage
from state_machine import Form

bot = Bot(get_token(), parse_mode=ParseMode.HTML)
router = Router()

dp = Dispatcher()
dp.include_router(router)


@router.message(Command('change_password'))
async def change_group(message: types.Message, state: FSMContext):
    if message.chat.id == int(db.group_id):
        await state.set_state(Form.check_old_password)
        await message.answer(answerMessage.pleaseSendUsOldPassword)


@router.message(Form.check_old_password)
async def check_old_password(message: types.Message, state: FSMContext):
    db.collection = db.get_collection().find_one()
    if db.collection['password'] == message.text:
        await state.set_state(Form.get_new_password)
        await message.answer(answerMessage.pleaseSendUsNewPassword)
    else:
        await message.answer(answerMessage.pleaseSendUsOldPassword)
    del db.collection


@router.message(Form.get_new_password)
async def get_new_password(message: types.Message, state: FSMContext):
    await state.clear()
    db.collection = db.get_collection()
    db.collection.update_one({"_id": 0}, {"$set": {"password": message.text}})
    # db.changeDb(f"UPDATE main SET password='{message.text}' WHERE id_number=0")
    await message.answer(answerMessage.passwordHaveBeenChanged)


@router.message(F.text.contains(db.get_db_password()))
async def create_channel_for_reporting(message: types.Message):
    if message.chat.type in {'group', 'supergroup'}:
        db.collection = db.get_collection()
        db.collection.update_one({"_id": 0}, {"$set": {"group_id": message.chat.id}})
        del db.collection
        # db.changeDb(f"UPDATE main SET group_id='{message.chat.id}' WHERE id_number=0")
        db.group_id = message.chat.id

        await message.answer(answerMessage.chatHaveBeenChanged)


@router.message()
async def echo_handler(message: types.Message):
    if db.group_id != '0':
        if message.chat.type in {'group', 'supergroup'}:
            if any(word in message.text for word in answerMessage.random_words):
                await bot.send_message(db.group_id, message.text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=1, stream=sys.stdout)
    asyncio.run(main())
