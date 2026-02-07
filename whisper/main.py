import asyncio
import discord
from discord import app_commands
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# --- КОНФИГУРАЦИЯ ---
TG_TOKEN = 'ТВОЙ_ТГ_ТОКЕН'
DS_TOKEN = 'ТВОЙ_ДС_ТОКЕН'

# Инициализация Telegram
tg_bot = Bot(token=TG_TOKEN)
dp = Dispatcher(tg_bot)

# Инициализация Discord
class DiscordClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

ds_client = DiscordClient()

# --- ЛОГИКА TELEGRAM (Inline Whisper) ---
@dp.inline_handler()
async def tg_inline_whisper(inline_query: types.InlineQuery):
    query = inline_query.query.split(maxsplit=1)
    if len(query) < 2:
        return

    target_user = query[0]  # Например, @username
    secret_text = query[1]

    results = [
        types.InlineQueryResultArticle(
            id='1',
            title=f"Шепот для {target_user}",
            input_message_content=types.InputTextMessageContent(
                f"🤫 Секретное сообщение для {target_user}..."
            ),
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(
                    "Открыть 🔓", 
                    callback_data=f"whisper:{target_user}:{secret_text}"
                )
            )
        )
    ]
    await tg_bot.answer_inline_query(inline_query.id, results=results, cache_time=1)

@dp.callback_query_handler(lambda c: c.data.startswith('whisper:'))
async def process_whisper(callback_query: types.CallbackQuery):
    _, target, text = callback_query.data.split(':', 2)
    
    # Проверка, тот ли это пользователь (по username)
    if f"@{callback_query.from_user.username}" == target:
        await callback_query.answer(text, show_alert=True)
    else:
        await callback_query.answer("Это сообщение не для тебя! ❌", show_alert=True)

# --- ЛОГИКА DISCORD (Slash Command) ---
@ds_client.tree.command(name="whisper", description="Отправить секрет")
async def ds_whisper(interaction: discord.Interaction, target: discord.Member, message: str):
    # В дискорде отправляем уведомление в чат, а текст — в ЛС
    await interaction.response.send_message(
        f"🤫 {interaction.user.mention} отправил секрет для {target.mention}!", 
        ephemeral=False 
    )
    try:
        await target.send(f"✉️ Тебе шепнули в Discord: {message}")
    except:
        await interaction.followup.send("Не удалось отправить ЛС (закрыто у юзера)", ephemeral=True)

# --- ЗАПУСК ОБОИХ БОТОВ ---
async def main():
    # Запускаем Discord в фоне
    loop = asyncio.get_event_loop()
    loop.create_task(ds_client.start(DS_TOKEN))
    
    # Запускаем Telegram (polling)
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
