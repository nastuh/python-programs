import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Конфигурация
API_TOKEN = 'your_token'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# База данных в оперативной памяти (в реальном проекте лучше использовать БД)
user_data = {}

def get_profile(user_id):
    if user_id not in user_data:
        user_data[user_id] = {
            "distance": 0,
            "items": [],
            "level": 1
        }
    return user_data[user_id]

def get_swim_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Плыть 🌊", 
        callback_data="swim")
    )
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "|Вы находитесь на берегу| |🏝|\nНачните свое путешествие прямо сейчас.",
        reply_markup=get_swim_keyboard()
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "**Команды бота:**\n"
        "- `/start` — Начать путешествие\n"
        "- `/me` — Посмотреть свой профиль и инвентарь\n"
        "- `/help` — Справка по игре\n\n"
        "Нажимай кнопку 'Плыть', чтобы преодолевать расстояние и находить артефакты."
    )
    await message.answer(help_text, parse_mode="Markdown")

@dp.message(Command("me"))
async def cmd_profile(message: types.Message):
    profile = get_profile(message.from_user.id)
    items_str = ", ".join(profile["items"]) if profile["items"] else "Пусто"
    
    profile_text = (
        f"**Профиль исследователя** {{joy}}\n"
        f"- Пройдено: `{profile['distance']} метров`\n"
        f"- Уровень: `{profile['level']}`\n"
        f"- Вещи: _{items_str}_"
    )
    await message.answer(profile_text, parse_mode="Markdown")

@dp.callback_query(F.data == "swim")
async def process_swim(callback: types.CallbackQuery):
    profile = get_profile(callback.from_user.id)
    
    # Увеличиваем дистанцию
    add_distance = random.randint(5, 15)
    profile["distance"] += add_distance
    
    # Логика уровней
    profile["level"] = (profile["distance"] // 100) + 1
    
    event_text = ""
    # Шанс найти вещь (15%)
    if random.random() < 0.15:
        loot = random.choice(["Древняя монета", "Ржавый ключ", "Черная жемчужина", "Обломок весла", "Карта сокровищ"])
        profile["items"].append(loot)
        event_text = f"\n\n✨ **Ого! Вы нашли:** `{loot}`"

    try:
        await callback.message.edit_text(
            f"|Вы плывете| |✅|\nДистанция: `{profile['distance']} м`{event_text}",
            reply_markup=get_swim_keyboard(),
            parse_mode="Markdown"
        )
    except Exception:
        # Игнорируем ошибку, если текст сообщения не изменился
        pass
    
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
