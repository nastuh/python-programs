
import logging
import hashlib
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Твой токен
API_TOKEN = '8504339437:AAGT8etG6JKBNEARMKl-YV9b9yEcS65BjHs'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Хранилище для шепотов
whispers = {}

@dp.inline_query()
async def inline_whisper(inline_query: InlineQuery):
    text = inline_query.query.strip()
    
    if not text or not text.startswith('@'):
        return

    try:
        # Разбиваем строку: @username сообщение
        parts = text.split(' ', 1)
        target_user = parts[0].replace('@', '').lower()
        message = parts[1] if len(parts) > 1 else "..."
    except Exception:
        return

    # Уникальный ID
    whisper_id = hashlib.md5(text.encode()).hexdigest()
    whispers[whisper_id] = {
        'target': target_user,
        'message': message,
        'sender': inline_query.from_user.full_name
    }

    # Кнопка
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Посмотреть шепот 🔓", callback_data=f"read_{whisper_id}")]
    ])

    results = [
        InlineQueryResultArticle(
            id=whisper_id,
            title=f"Шепот для @{target_user}",
            description="Только он(а) сможет прочитать",
            input_message_content=InputTextMessageContent(
                message_text=f"🤫 У меня есть секрет для @{target_user}..."
            ),
            reply_markup=kb
        )
    ]
    
    await inline_query.answer(results=results, cache_time=1)

@dp.callback_query(F.data.startswith('read_'))
async def process_callback_read(callback_query: CallbackQuery):
    whisper_id = callback_query.data.split('_')[1]
    whisper = whispers.get(whisper_id)

    if not whisper:
        await callback_query.answer("Секрет не найден или бот перезагружен.", show_alert=True)
        return

    # Проверяем username (без учета регистра)
    current_user = callback_query.from_user.username.lower() if callback_query.from_user.username else ""
    
    if current_user == whisper['target']:
        await callback_query.answer(f"От {whisper['sender']}:\n{whisper['message']}", show_alert=True)
    else:
        await callback_query.answer("Это не для тебя! 🤐", show_alert=True)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")