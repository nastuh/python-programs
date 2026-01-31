import asyncio
import discord
from discord.ext import commands
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# --- НАСТРОЙКИ (ЗАМЕНИТЕ НА СВОИ) ---
TG_TOKEN = '8310589058:AAGKQdGgpqJbD-wBA98uxozSNPOdYRYG5OA'
DC_TOKEN = 'MTQzNzcxMTM2MTMyODI4MzcwMA.GvutkW.A04e55bjrkA94wXu0Q6qigzpfUCETNWUwTZHaw'
TG_CHAT_ID = -1005133542087 # ID чата/канала Telegram
DC_CHANNEL_ID = 1405664986763624558 # ID канала Discord

# --- ИНИЦИАЛИЗАЦИЯ БОТОВ ---
tg_bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

# Настраиваем Discord бота. ВАЖНО: включить права на чтение сообщений!
intents = discord.Intents.default()
intents.message_content = True
dc_bot = commands.Bot(command_prefix="!", intents=intents)

# --- ЯДРО СИНХРОНИЗАЦИИ ---
# 1. Из Telegram в Discord
@dp.message()
async def telegram_to_discord(message: types.Message):
    # Пересылаем только сообщения из нужного чата и не от ботов
    if message.chat.id == TG_CHAT_ID and not message.from_user.is_bot:
        # Игнорируем команды (сообщения, начинающиеся с "/")
        if message.text and message.text.startswith('/'):
            return

        # Формируем текст для Discord
        user_name = message.from_user.full_name
        text = message.text or message.caption or ""

        # Добавляем метку для медиа-файлов
        if message.photo:
            text = text + " 📸 [Фото]"
        elif message.video:
            text = text + " 🎥 [Видео]"
        elif message.document:
            text = text + f" 📄 [Документ]"
        elif message.sticker:
            text = text + " ✨ [Стикер]"

        # Отправляем в Discord
        channel = dc_bot.get_channel(DC_CHANNEL_ID)
        if channel:
            await channel.send(f"**[{user_name}]** {text}")

# 2. Из Discord в Telegram
@dc_bot.event
async def on_message(message):
    # Пересылаем только сообщения из нужного канала, не от ботов и не команды
    if (message.channel.id == DC_CHANNEL_ID and 
        not message.author.bot and 
        not message.content.startswith(dc_bot.command_prefix)):
        
        # Формируем текст для Telegram
        user_name = message.author.display_name
        text = message.content

        # Добавляем метку для вложений
        if message.attachments:
            text = text + " 📎 [Вложение]"

        # Отправляем в Telegram
        await tg_bot.send_message(
            chat_id=TG_CHAT_ID,
            text=f"**[{user_name}]** {text}"
        )
    
    # Позволяем другим командам бота работать
    await dc_bot.process_commands(message)

# --- МИНИМАЛЬНЫЕ КОМАНДЫ ДЛЯ УДОБСТВА ---
@dc_bot.command(name='пинг')
async def ping(ctx):
    """Просто проверяем, что бот жив в Discord"""
    await ctx.send('Понг! Синхронизация активна.')

@dp.message(Command("старт"))
async def start(message: types.Message):
    """Команда для проверки бота в Telegram"""
    await message.answer("Бот работает. Сообщения синхронизируются с Discord.")

# --- ЗАПУСК ---
async def main():
    # Запускаем оба бота параллельно
    await asyncio.gather(
        dc_bot.start(DC_TOKEN),
        dp.start_polling(tg_bot, skip_updates=True)
    )

if __name__ == "__main__":
    asyncio.run(main())