#!/usr/bin/env python3
import logging
import sys

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ВАЖНО: замените на ваш токен бота
BOT_TOKEN = "your_token"

# Простое хранилище в памяти
user_data = {}

def main_menu():
    """Главное меню"""
    keyboard = [
        [InlineKeyboardButton("📝 Создать заметку", callback_data="add_note")],
        [InlineKeyboardButton("✅ Создать список", callback_data="add_todo")],
        [InlineKeyboardButton("📒 Мои заметки", callback_data="view_notes")],
        [InlineKeyboardButton("📋 Мои списки", callback_data="view_todos")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /start"""
    user = update.effective_user
    
    await update.message.reply_text(
        f"✨ Привет, {user.first_name}! ✨\n\n"
        "Я бот для заметок и задач.\n"
        "Выбери действие:",
        reply_markup=main_menu()
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий кнопок"""
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    # Инициализируем данные пользователя, если их нет
    if user_id not in user_data:
        user_data[user_id] = {
            'notes': [],
            'todos': []
        }
    
    if query.data == "add_note":
        await query.edit_message_text(
            "📝 *Создание заметки*\n\n"
            "Введите текст заметки:",
            parse_mode="Markdown"
        )
        context.user_data['awaiting_note'] = True
    
    elif query.data == "add_todo":
        await query.edit_message_text(
            "📋 *Создание списка дел*\n\n"
            "Введите название списка:",
            parse_mode="Markdown"
        )
        context.user_data['awaiting_todo_title'] = True
    
    elif query.data == "view_notes":
        notes = user_data[user_id]['notes']
        
        if not notes:
            keyboard = [[InlineKeyboardButton("📝 Создать заметку", callback_data="add_note")]]
            await query.edit_message_text(
                "📭 У вас пока нет заметок.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return
        
        text = "📒 *Ваши заметки:*\n\n"
        for i, note in enumerate(notes, 1):
            text += f"{i}. {note}\n"
        
        keyboard = [
            [InlineKeyboardButton("📝 Новая заметка", callback_data="add_note")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif query.data == "view_todos":
        todos = user_data[user_id]['todos']
        
        if not todos:
            keyboard = [[InlineKeyboardButton("✅ Создать список", callback_data="add_todo")]]
            await query.edit_message_text(
                "📭 У вас пока нет списков дел.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return
        
        text = "📋 *Ваши списки дел:*\n\n"
        for i, todo in enumerate(todos, 1):
            text += f"{i}. *{todo['title']}*\n"
            for j, item in enumerate(todo['items'], 1):
                text += f"   {j}. {item}\n"
            text += "\n"
        
        keyboard = [
            [InlineKeyboardButton("✅ Новый список", callback_data="add_todo")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif query.data == "main_menu":
        await query.edit_message_text(
            "🏠 *Главное меню*\n\nВыберите действие:",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений"""
    user_id = str(update.effective_user.id)
    text = update.message.text.strip()
    
    # Инициализируем данные пользователя, если их нет
    if user_id not in user_data:
        user_data[user_id] = {
            'notes': [],
            'todos': []
        }
    
    if context.user_data.get('awaiting_note'):
        # Сохраняем заметку
        user_data[user_id]['notes'].append(text)
        
        # Очищаем состояние
        context.user_data.pop('awaiting_note', None)
        
        keyboard = [
            [InlineKeyboardButton("📒 Все заметки", callback_data="view_notes")],
            [InlineKeyboardButton("📝 Новая заметка", callback_data="add_note")]
        ]
        
        await update.message.reply_text(
            f"✅ *Заметка сохранена!*\n\n{text}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif context.user_data.get('awaiting_todo_title'):
        # Начинаем создание списка
        context.user_data['todo_title'] = text
        context.user_data['todo_items'] = []
        context.user_data.pop('awaiting_todo_title', None)
        context.user_data['awaiting_todo_item'] = True
        
        await update.message.reply_text(
            f"📋 *Список '{text}' создан!*\n\n"
            "Теперь добавляйте пункты (по одному в сообщении).\n"
            "Когда закончите, напишите 'готово'.",
            parse_mode="Markdown"
        )
    
    elif context.user_data.get('awaiting_todo_item'):
        if text.lower() == 'готово':
            # Завершаем создание списка
            title = context.user_data['todo_title']
            items = context.user_data['todo_items']
            
            user_data[user_id]['todos'].append({
                'title': title,
                'items': items
            })
            
            # Красиво оформляем список
            formatted = f"📋 *{title}*\n\n"
            for i, item in enumerate(items, 1):
                formatted += f"{i}. {item}\n"
            
            keyboard = [
                [InlineKeyboardButton("📋 Все списки", callback_data="view_todos")],
                [InlineKeyboardButton("✅ Новый список", callback_data="add_todo")]
            ]
            
            await update.message.reply_text(
                f"✅ *Список сохранен!*\n\n{formatted}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            
            # Очищаем состояние
            context.user_data.clear()
        
        else:
            # Добавляем пункт в список
            context.user_data['todo_items'].append(text)
            count = len(context.user_data['todo_items'])
            
            await update.message.reply_text(
                f"✅ *Добавлено:* {text}\n"
                f"📊 Всего пунктов: {count}\n\n"
                "Добавляйте ещё или напишите 'готово'.",
                parse_mode="Markdown"
            )

def main():
    """Основная функция запуска бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    logger.info("Бот запускается...")
    application.run_polling()

if __name__ == "__main__":
    main()
