
import json
import os
import logging
from typing import Dict, List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.error import NetworkError


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "your_token"


DATA_FILE = "bot_data.json"

class NotesBot:
    def __init__(self):
        self.user_data = self.load_data()
    
    def load_data(self) -> Dict:
       
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Ошибка загрузки данных: {e}")
        return {}
    
    def save_data(self):
        
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Ошибка сохранения данных: {e}")
    
    def get_user_data(self, user_id: str) -> Dict:
        
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                'notes': [],
                'todos': []
            }
            self.save_data()
        return self.user_data[user_id]
    
    def main_menu(self):
        
        keyboard = [
            [InlineKeyboardButton("📝 Новая заметка", callback_data="add_note")],
            [InlineKeyboardButton("📋 Новый список", callback_data="add_todo")],
            [InlineKeyboardButton("📄 Мои заметки", callback_data="view_notes")],
            [InlineKeyboardButton("✅ Мои списки", callback_data="view_todos")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        user = update.effective_user
        
        text = (
            f"👋 Привет, {user.first_name}!\n\n"
            "📌 Бот для заметок и списков дел.\n\n"
            "✅ Все данные сохраняются автоматически\n"
            "📱 Удобные кнопки управления\n"
            "🎯 Отмечайте выполненные задачи\n\n"
            "Выберите действие:"
        )
        
        await update.message.reply_text(text, reply_markup=self.main_menu())
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        query = update.callback_query
        await query.answer()
        
        user_id = str(query.from_user.id)
        data = query.data
        
        if data == "add_note":
            await query.edit_message_text(
                "✏️ <b>Создание заметки</b>\n\nВведите текст заметки:",
                parse_mode="HTML"
            )
            context.user_data['awaiting_note'] = True
        
        elif data == "add_todo":
            await query.edit_message_text(
                "📋 <b>Создание списка</b>\n\nВведите название списка:",
                parse_mode="HTML"
            )
            context.user_data['awaiting_todo_title'] = True
        
        elif data == "view_notes":
            await self.show_notes(query, user_id)
        
        elif data == "view_todos":
            await self.show_todos_overview(query, user_id)
        
        elif data.startswith("view_todo_"):
            list_index = int(data.split("_")[2])
            await self.show_todo_details(query, user_id, list_index)
        
        elif data.startswith("complete_"):
            parts = data.split("_")
            list_index = int(parts[1])
            item_index = int(parts[2])
            await self.toggle_task(query, user_id, list_index, item_index)
        
        elif data.startswith("delete_note_"):
            note_index = int(data.split("_")[2])
            await self.delete_note(query, user_id, note_index)
        
        elif data.startswith("delete_todo_"):
            list_index = int(data.split("_")[2])
            await self.delete_todo(query, user_id, list_index)
        
        elif data.startswith("add_item_"):
            list_index = int(data.split("_")[2])
            await query.edit_message_text(
                "➕ <b>Добавление задачи</b>\n\nВведите текст задачи:",
                parse_mode="HTML"
            )
            context.user_data['awaiting_todo_item'] = True
            context.user_data['current_list_index'] = list_index
        
        elif data == "back_to_menu":
            await query.edit_message_text(
                "📋 <b>Главное меню</b>\n\nВыберите действие:",
                parse_mode="HTML",
                reply_markup=self.main_menu()
            )
    
    async def show_notes(self, query, user_id: str):
        
        user_data = self.get_user_data(user_id)
        notes = user_data['notes']
        
        if not notes:
            keyboard = [[InlineKeyboardButton("📝 Новая заметка", callback_data="add_note")]]
            await query.edit_message_text(
                "📭 <b>Нет заметок</b>\n\nСоздайте первую заметку!",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return
        
        text = "📄 <b>Ваши заметки:</b>\n\n"
        
        for i, note in enumerate(notes):
            note_text = note[:60] + "..." if len(note) > 60 else note
            text += f"<b>{i+1}.</b> {note_text}\n"
        
        
        keyboard = []
        
       
        for i in range(min(5, len(notes))):
            keyboard.append([
                InlineKeyboardButton(f"👁️ Заметка {i+1}", callback_data=f"view_note_{i}"),
                InlineKeyboardButton(f"🗑️ Удалить", callback_data=f"delete_note_{i}")
            ])
        
        keyboard.append([
            InlineKeyboardButton("📝 Новая заметка", callback_data="add_note"),
            InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")
        ])
        
        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def show_todos_overview(self, query, user_id: str):
        
        user_data = self.get_user_data(user_id)
        todos = user_data['todos']
        
        if not todos:
            keyboard = [[InlineKeyboardButton("📋 Новый список", callback_data="add_todo")]]
            await query.edit_message_text(
                "📭 <b>Нет списков</b>\n\nСоздайте первый список!",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return
        
        text = "✅ <b>Ваши списки:</b>\n\n"
        
        for i, todo in enumerate(todos):
            completed = sum(1 for item in todo['items'] if item.get('completed', False))
            total = len(todo['items'])
            
            text += f"<b>{i+1}. {todo['title']}</b>\n"
            if total > 0:
                filled = int((completed / total) * 8)
                progress_bar = "█" * filled + "░" * (8 - filled)
                percentage = (completed / total) * 100
                text += f"   {progress_bar} {completed}/{total} ({percentage:.0f}%)\n"
            else:
                text += "   📭 Список пуст\n"
            
            
            for item in todo['items'][:3]:
                status = "✓" if item.get('completed', False) else "○"
                item_text = item['text'][:25]
                if len(item['text']) > 25:
                    item_text += "..."
                text += f"   {status} {item_text}\n"
            
            text += "\n"
        
        
        keyboard = []
        
       
        for i in range(min(3, len(todos))):
            keyboard.append([
                InlineKeyboardButton(f"👁️ Список {i+1}", callback_data=f"view_todo_{i}"),
                InlineKeyboardButton(f"➕ Задачи", callback_data=f"add_item_{i}"),
                InlineKeyboardButton(f"🗑️ Удалить", callback_data=f"delete_todo_{i}")
            ])
        
        keyboard.append([
            InlineKeyboardButton("📋 Новый список", callback_data="add_todo"),
            InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")
        ])
        
        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def show_todo_details(self, query, user_id: str, list_index: int):
        
        user_data = self.get_user_data(user_id)
        todos = user_data['todos']
        
        if list_index >= len(todos):
            await query.edit_message_text("❌ Список не найден")
            return
        
        todo = todos[list_index]
        
       
        completed = sum(1 for item in todo['items'] if item.get('completed', False))
        total = len(todo['items'])
        
        text = f"📋 <b>{todo['title']}</b>\n\n"
        
        if total > 0:
            filled = int((completed / total) * 10)
            progress_bar = "█" * filled + "░" * (10 - filled)
            percentage = (completed / total) * 100
            text += f"{progress_bar} {completed}/{total} ({percentage:.0f}%)\n\n"
        
        
        if not todo['items']:
            text += "📭 Список пуст\n"
        else:
            for i, item in enumerate(todo['items'], 1):
                status = "✅" if item.get('completed', False) else "⭕"
                text += f"<b>{i}.</b> {status} {item['text']}\n"
        
       
        keyboard = []
        
        
        row = []
        for i in range(len(todo['items'])):
            status = "✓" if todo['items'][i].get('completed', False) else "○"
            btn_text = f"{status}{i+1}"  
            row.append(InlineKeyboardButton(btn_text, callback_data=f"complete_{list_index}_{i}"))
            
            
            if len(row) == 5 or i == len(todo['items']) - 1:
                keyboard.append(row)
                row = []
        
       
        keyboard.append([
            InlineKeyboardButton("➕ Добавить задачу", callback_data=f"add_item_{list_index}"),
            InlineKeyboardButton("🔙 К спискам", callback_data="view_todos")
        ])
        
        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def toggle_task(self, query, user_id: str, list_index: int, item_index: int):
        
        user_data = self.get_user_data(user_id)
        
        if list_index < len(user_data['todos']) and item_index < len(user_data['todos'][list_index]['items']):
            item = user_data['todos'][list_index]['items'][item_index]
            item['completed'] = not item.get('completed', False)
            self.save_data()
            
            await self.show_todo_details(query, user_id, list_index)
    
    async def delete_note(self, query, user_id: str, note_index: int):
       
        user_data = self.get_user_data(user_id)
        
        if note_index < len(user_data['notes']):
            del user_data['notes'][note_index]
            self.save_data()
            
            keyboard = [[InlineKeyboardButton("🔙 К заметкам", callback_data="view_notes")]]
            await query.edit_message_text(
                "🗑️ <b>Заметка удалена</b>",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
    async def delete_todo(self, query, user_id: str, list_index: int):
        
        user_data = self.get_user_data(user_id)
        
        if list_index < len(user_data['todos']):
            del user_data['todos'][list_index]
            self.save_data()
            
            keyboard = [[InlineKeyboardButton("🔙 К спискам", callback_data="view_todos")]]
            await query.edit_message_text(
                "🗑️ <b>Список удален</b>",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
      
        user_id = str(update.effective_user.id)
        text = update.message.text.strip()
        
        if context.user_data.get('awaiting_note'):
            
            user_data = self.get_user_data(user_id)
            user_data['notes'].append(text)
            self.save_data()
            
            context.user_data.pop('awaiting_note', None)
            
            await update.message.reply_text(
                f"✅ <b>Заметка сохранена!</b>\n\n{text}",
                parse_mode="HTML",
                reply_markup=self.main_menu()
            )
        
        elif context.user_data.get('awaiting_todo_title'):
           
            new_todo = {
                'title': text,
                'items': []
            }
            
            user_data = self.get_user_data(user_id)
            user_data['todos'].append(new_todo)
            self.save_data()
            
            list_index = len(user_data['todos']) - 1
            context.user_data.pop('awaiting_todo_title', None)
            context.user_data['current_list_index'] = list_index
            context.user_data['awaiting_todo_item'] = True
            
            keyboard = [[InlineKeyboardButton("➕ Добавить первую задачу", callback_data=f"add_item_{list_index}")]]
            
            await update.message.reply_text(
                f"📋 <b>Список создан!</b>\n\n"
                f"Название: {text}\n\n"
                f"Теперь добавляйте задачи. Каждое сообщение - новая задача.\n"
                f"Напишите 'готово' чтобы завершить.",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        elif context.user_data.get('awaiting_todo_item'):
            if text.lower() in ['готово', 'завершить', 'стоп']:
              
                context.user_data.clear()
                
                user_data = self.get_user_data(user_id)
                list_index = context.user_data.get('current_list_index')
                
                if list_index is not None and list_index < len(user_data['todos']):
                    todo = user_data['todos'][list_index]
                    formatted_list = self.format_todo_for_display(todo)
                    
                    keyboard = [
                        [InlineKeyboardButton("✅ Просмотреть", callback_data=f"view_todo_{list_index}")],
                        [InlineKeyboardButton("➕ Новый список", callback_data="add_todo")]
                    ]
                    
                    await update.message.reply_text(
                        f"✅ <b>Список завершен!</b>\n\n{formatted_list}",
                        parse_mode="HTML",
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    )
                else:
                    await update.message.reply_text(
                        "✅ <b>Создание списка завершено!</b>",
                        parse_mode="HTML",
                        reply_markup=self.main_menu()
                    )
            
            else:
             
                list_index = context.user_data.get('current_list_index')
                if list_index is not None:
                    user_data = self.get_user_data(user_id)
                    
                    if list_index < len(user_data['todos']):
                        todo = user_data['todos'][list_index]
                        
                        new_item = {
                            'text': text,
                            'completed': False
                        }
                        
                        todo['items'].append(new_item)
                        self.save_data()
                        
                        item_number = len(todo['items'])
                        formatted_list = self.format_todo_for_display(todo)
                        
                        keyboard = [
                            [InlineKeyboardButton("➕ Ещё задача", callback_data=f"add_item_{list_index}")],
                            [InlineKeyboardButton("✅ Готово", callback_data=f"finish_todo_{list_index}")]
                        ]
                        
                        await update.message.reply_text(
                            f"✅ <b>Задача {item_number} добавлена!</b>\n\n{formatted_list}\n\n"
                            f"Продолжайте или напишите 'готово'.",
                            parse_mode="HTML",
                            reply_markup=InlineKeyboardMarkup(keyboard)
                        )
    
    def format_todo_for_display(self, todo: Dict) -> str:
        
        text = f"📋 <b>{todo['title']}</b>\n\n"
        
        if not todo['items']:
            text += "📭 Список пуст\n"
        else:
            for i, item in enumerate(todo['items'], 1):
                status = "✓" if item.get('completed', False) else "○"
                text += f"<b>{i}.</b> {status} {item['text']}\n"
        
        return text

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    
    logger.error(f"Ошибка: {context.error}", exc_info=context.error)
    
    if isinstance(context.error, NetworkError):
        logger.warning("Сетевая ошибка, продолжаю работу...")
    else:
        logger.error(f"Необработанная ошибка: {context.error}")

def main():

    bot = NotesBot()
    
  
    app = Application.builder().token(BOT_TOKEN).build()
    
 
    app.add_error_handler(error_handler)
    
  
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CallbackQueryHandler(bot.handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    

    logger.info("Запускаю бота...")
    try:
        app.run_polling(
            poll_interval=1.0,
            timeout=30,
            drop_pending_updates=True
        )
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise

if __name__ == "__main__":
    main()
