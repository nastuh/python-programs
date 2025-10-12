import logging
from datetime import datetime, time
from typing import Dict, List

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, 
                      InlineKeyboardButton, Update)
from telegram.ext import (Application, CommandHandler, ContextTypes, ConversationHandler,
                          MessageHandler, filters, CallbackQueryHandler, JobQueue)

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
(
    CHOOSING, ADD_RECORD, DELETE_RECORD, EDIT_RECORD, 
    SELECT_CATEGORY, ADD_TO_LIST, LIST_CHOICE, DELETE_FROM_LIST
) = range(8)

# Emojis for UI
EMOJIS = {
    'notebook': '📔',
    'add': '➕',
    'delete': '➖',
    'edit': '✏️',
    'list': '📋',
    'back': '🔙',
    'done': '✅',
    'categories': '📂',
    'time': '⏰',
    'error': '❌',
    'warning': '⚠️',
    'calendar': '📅',
    'movie': '🎬',
    'drama': '📺',
    'manga': '📘',
    'series': '🍿',
    'fanfic': '📖',
    'lists': '📝'
}

# Categories with emojis
CATEGORIES = {
    'work': '💼 Work',
    'personal': '👨‍💻 Personal',
    'shopping': '🛍️ Shopping',
    'ideas': '💡 Ideas',
    'health': '🏥 Health'
}

# List types
LIST_TYPES = {
    'drama': f"{EMOJIS['drama']} Dramas",
    'manga': f"{EMOJIS['manga']} Manga",
    'movie': f"{EMOJIS['movie']} Movies",
    'series': f"{EMOJIS['series']} TV Series",
    'fanfic': f"{EMOJIS['fanfic']} Fanfics"
}

# User data storage
user_data = {}

def get_today_date():
    """Returns today's date in DD.MM.YYYY format"""
    return datetime.now().strftime("%d.%m.%Y")

def get_user_notes(user_id: int):
    """Gets or creates user's notes"""
    if user_id not in user_data:
        user_data[user_id] = {
            'notes': {},
            'categories': list(CATEGORIES.keys()),
            'reminder_time': time(20, 0),
            'lists': {
                'drama': [],
                'manga': [],
                'movie': [],
                'series': [],
                'fanfic': []
            }
        }
    return user_data[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation with main menu."""
    user = update.message.from_user if update.message else update.callback_query.from_user
    logger.info("User %s started the conversation.", user.first_name)
    
    welcome_message = (
        f"{EMOJIS['notebook']} <b>Welcome to Notebook Bot!</b>\n\n"
        "I'm your personal organizer bot that helps you:\n"
        "- 📝 Keep notes with categories\n"
        "- 📅 Organize by dates\n"
        "- 📺 Track your watchlists (dramas, movies, etc.)\n"
        "- ⏰ Set daily reminders\n\n"
        "Choose what you'd like to do:"
    )
    
    reply_keyboard = [
        [f"{EMOJIS['add']} Add Note", f"{EMOJIS['delete']} Delete Note"],
        [f"{EMOJIS['edit']} Edit Note", f"{EMOJIS['list']} View Notes"],
        [f"{EMOJIS['categories']} Categories", f"{EMOJIS['lists']} My Lists"],
        [f"{EMOJIS['time']} Reminders"]
    ]

    if update.callback_query:
        await update.callback_query.edit_message_text(
            welcome_message,
            parse_mode="HTML",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            )
        )
    else:
        await update.message.reply_text(
            welcome_message,
            parse_mode="HTML",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            )
        )

    return CHOOSING

async def add_record(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts adding a new note."""
    user = update.message.from_user if update.message else update.callback_query.from_user
    
    message = (
        f"{EMOJIS['add']} <b>Adding a New Note</b>\n\n"
        "Please type your note below. You'll be able to categorize it next."
    )
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )
    
    return ADD_RECORD

async def save_record(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the note and asks for category."""
    user = update.message.from_user
    text = update.message.text
    user_notes = get_user_notes(user.id)
    
    # Save text temporarily
    context.user_data['temp_note'] = text
    
    # Create category keyboard
    keyboard = []
    for category in user_notes['categories']:
        keyboard.append([InlineKeyboardButton(CATEGORIES[category], callback_data=f"category_{category}")])
    
    keyboard.append([InlineKeyboardButton(f"{EMOJIS['back']} Back", callback_data="back")])
    
    await update.message.reply_text(
        f"{EMOJIS['categories']} <b>Select a category for your note:</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return SELECT_CATEGORY

async def category_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles category selection and saves note."""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    user_notes = get_user_notes(user.id)
    
    if query.data == "back":
        return await start(update, context)
    
    # Get category from callback_data (format "category_work")
    category = query.data.split('_')[1]
    note_text = context.user_data['temp_note']
    
    # Get current date
    today = get_today_date()
    
    # Add note
    if today not in user_notes['notes']:
        user_notes['notes'][today] = []
    
    user_notes['notes'][today].append({
        'text': note_text,
        'category': category,
        'created_at': datetime.now().strftime("%H:%M")
    })
    
    await query.edit_message_text(
        f"{EMOJIS['done']} <b>Note added successfully!</b>\n\n"
        f"{EMOJIS['calendar']} <b>Date:</b> {today}\n"
        f"{CATEGORIES[category]}\n"
        f"<b>Text:</b> {note_text}",
        parse_mode="HTML"
    )
    
    # Send new message with main menu
    reply_keyboard = [
        [f"{EMOJIS['add']} Add Note", f"{EMOJIS['delete']} Delete Note"],
        [f"{EMOJIS['edit']} Edit Note", f"{EMOJIS['list']} View Notes"],
        [f"{EMOJIS['categories']} Categories", f"{EMOJIS['lists']} My Lists"],
        [f"{EMOJIS['time']} Reminders"]
    ]
    
    await context.bot.send_message(
        chat_id=user.id,
        text="What would you like to do next?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        )
    )
    
    return CHOOSING

async def delete_record(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Shows notes for deletion."""
    user = update.message.from_user if update.message else update.callback_query.from_user
    user_notes = get_user_notes(user.id)
    
    if not user_notes['notes']:
        if update.callback_query:
            await update.callback_query.edit_message_text(
                f"{EMOJIS['warning']} You don't have any notes to delete yet."
            )
        else:
            await update.message.reply_text(
                f"{EMOJIS['warning']} You don't have any notes to delete yet.",
                reply_markup=ReplyKeyboardMarkup([[f"{EMOJIS['back']} Back"]], resize_keyboard=True)
            )
        return CHOOSING
    
    # Create keyboard with notes
    keyboard = []
    for date, notes in user_notes['notes'].items():
        for i, note in enumerate(notes):
            keyboard.append([
                InlineKeyboardButton(
                    f"{date} - {note['text'][:20]}...",
                    callback_data=f"delete_{date}_{i}"
                )
            ])
    
    keyboard.append([InlineKeyboardButton(f"{EMOJIS['back']} Back", callback_data="back")])
    
    message = (
        f"{EMOJIS['delete']} <b>Select a note to delete:</b>\n\n"
        "These are all your notes grouped by date:"
    )
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    return DELETE_RECORD

async def delete_record_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Deletes the selected note."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "back":
        return await start(update, context)
    
    user = query.from_user
    user_notes = get_user_notes(user.id)
    
    # Get data from callback_data (format "delete_DD.MM.YYYY_index")
    _, date, index = query.data.split('_')
    index = int(index)
    
    # Delete note
    deleted_note = user_notes['notes'][date].pop(index)
    
    # Remove date if no notes left
    if not user_notes['notes'][date]:
        del user_notes['notes'][date]
    
    await query.edit_message_text(
        f"{EMOJIS['done']} <b>Note deleted successfully!</b>\n\n"
        f"<b>Date:</b> {date}\n"
        f"<b>Content:</b> {deleted_note['text']}",
        parse_mode="HTML"
    )
    
    # Send new message with main menu
    reply_keyboard = [
        [f"{EMOJIS['add']} Add Note", f"{EMOJIS['delete']} Delete Note"],
        [f"{EMOJIS['edit']} Edit Note", f"{EMOJIS['list']} View Notes"],
        [f"{EMOJIS['categories']} Categories", f"{EMOJIS['lists']} My Lists"],
        [f"{EMOJIS['time']} Reminders"]
    ]
    
    await context.bot.send_message(
        chat_id=user.id,
        text="What would you like to do next?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        )
    )
    
    return CHOOSING

async def list_records(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows all user's notes."""
    user = update.message.from_user if update.message else update.callback_query.from_user
    user_notes = get_user_notes(user.id)
    
    if not user_notes['notes']:
        if update.callback_query:
            await update.callback_query.edit_message_text(
                f"{EMOJIS['warning']} You don't have any notes yet."
            )
        else:
            await update.message.reply_text(
                f"{EMOJIS['warning']} You don't have any notes yet.",
                reply_markup=ReplyKeyboardMarkup([[f"{EMOJIS['back']} Back"]], resize_keyboard=True)
            )
        return
    
    response = [f"{EMOJIS['notebook']} <b>Your Notes:</b>\n"]
    
    for date, notes in user_notes['notes'].items():
        response.append(f"\n{EMOJIS['calendar']} <b>{date}</b>")
        for note in notes:
            response.append(
                f"  {CATEGORIES[note['category']]} {EMOJIS['time']} {note['created_at']}\n"
                f"  - {note['text']}"
            )
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            "\n".join(response),
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text(
            "\n".join(response),
            parse_mode="HTML",
            reply_markup=ReplyKeyboardMarkup([[f"{EMOJIS['back']} Back"]], resize_keyboard=True)
        )

async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sets up daily reminder time."""
    user = update.message.from_user if update.message else update.callback_query.from_user
    
    message = (
        f"{EMOJIS['time']} <b>Set Daily Reminder</b>\n\n"
        "Please enter the time for your daily reminder in HH:MM format (e.g., 20:00).\n\n"
        "I'll send you a summary of your daily notes at this time."
    )
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )
    
    return CHOOSING

async def process_reminder_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processes the reminder time input."""
    user = update.message.from_user
    text = update.message.text
    
    try:
        # Parse time
        hour, minute = map(int, text.split(':'))
        reminder_time = time(hour, minute)
        
        # Save time for user
        user_notes = get_user_notes(user.id)
        user_notes['reminder_time'] = reminder_time
        
        # Remove old job if exists
        current_jobs = context.job_queue.get_jobs_by_name(str(user.id))
        for job in current_jobs:
            job.schedule_removal()
        
        # Set new job in JobQueue
        context.job_queue.run_daily(
            send_daily_reminder,
            time=reminder_time,
            days=tuple(range(7)),
            chat_id=user.id,
            name=str(user.id)
        )
        
        await update.message.reply_text(
            f"{EMOJIS['done']} <b>Reminder set successfully!</b>\n\n"
            f"I'll send you daily notes at {text}",
            parse_mode="HTML"
        )
    except (ValueError, IndexError):
        await update.message.reply_text(
            f"{EMOJIS['error']} <b>Invalid time format.</b>\n\n"
            "Please use HH:MM format (e.g., 20:00).",
            parse_mode="HTML"
        )
    
    return await start(update, context)

async def send_daily_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Sends daily reminder with today's notes."""
    job = context.job
    user_id = int(job.name)
    
    if user_id not in user_data:
        return
    
    user_notes = user_data[user_id]
    today = get_today_date()
    
    message = [f"{EMOJIS['notebook']} <b>Your Notes for Today ({today}):</b>"]
    
    if today in user_notes['notes']:
        for note in user_notes['notes'][today]:
            message.append(
                f"  {CATEGORIES[note['category']]} {EMOJIS['time']} {note['created_at']}\n"
                f"  - {note['text']}"
            )
    else:
        message.append(f"{EMOJIS['warning']} You don't have any notes for today.")
    
    await context.bot.send_message(job.chat_id, "\n".join(message), parse_mode="HTML")

async def show_lists_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Shows lists management menu."""
    user = update.message.from_user if update.message else update.callback_query.from_user
    
    message = (
        f"{EMOJIS['lists']} <b>My Lists Manager</b>\n\n"
        "Here you can manage your various lists:\n"
        "- Dramas 📺\n"
        "- Manga 📘\n"
        "- Movies 🎬\n"
        "- TV Series 🍿\n"
        "- Fanfics 📖\n\n"
        "Choose an action:"
    )
    
    reply_keyboard = [
        [f"{EMOJIS['add']} Add to List", f"{EMOJIS['list']} View Lists"],
        [f"{EMOJIS['delete']} Remove from List", f"{EMOJIS['back']} Back"]
    ]

    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode="HTML",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            )
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode="HTML",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            )
        )
    
    return LIST_CHOICE

async def choose_list_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Chooses list action."""
    user = update.message.from_user if update.message else update.callback_query.from_user
    action = update.message.text if update.message else None
    
    if not action:
        return await start(update, context)
    
    if action == f"{EMOJIS['back']} Back":
        return await start(update, context)
    
    # Determine selected action
    if action == f"{EMOJIS['add']} Add to List":
        context.user_data['list_action'] = 'add'
        return await choose_list_type(update, context)
    elif action == f"{EMOJIS['list']} View Lists":
        return await show_all_lists(update, context)
    elif action == f"{EMOJIS['delete']} Remove from List":
        context.user_data['list_action'] = 'delete'
        return await choose_list_type(update, context)
    else:
        return await start(update, context)

async def choose_list_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Chooses list type to work with."""
    user = update.message.from_user if update.message else update.callback_query.from_user
    
    message = (
        f"{EMOJIS['lists']} <b>Select List Type</b>\n\n"
        "Choose which list you want to manage:"
    )
    
    # Create keyboard with list types
    keyboard = []
    for list_type, list_name in LIST_TYPES.items():
        keyboard.append([InlineKeyboardButton(list_name, callback_data=f"list_{list_type}")])
    
    keyboard.append([InlineKeyboardButton(f"{EMOJIS['back']} Back", callback_data="back")])
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    return ADD_TO_LIST

async def list_type_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles list type selection."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "back":
        return await show_lists_menu(update, context)
    
    # Get list type from callback_data (format "list_drama")
    list_type = query.data.split('_')[1]
    context.user_data['current_list'] = list_type
    
    if context.user_data.get('list_action') == 'add':
        await query.edit_message_text(
            f"{LIST_TYPES[list_type]}\n\n"
            f"{EMOJIS['add']} <b>Add New Item</b>\n\n"
            "Please type the name of the item you want to add:",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )
        return ADD_TO_LIST
    else:
        return await prepare_delete_from_list(update, context)

async def add_to_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Adds item to selected list."""
    user = update.message.from_user
    text = update.message.text
    user_notes = get_user_notes(user.id)
    list_type = context.user_data['current_list']
    
    # Add item to list
    user_notes['lists'][list_type].append(text)
    
    await update.message.reply_text(
        f"{EMOJIS['done']} <b>Item added successfully!</b>\n\n"
        f"<b>List:</b> {LIST_TYPES[list_type]}\n"
        f"<b>Item:</b> {text}",
        parse_mode="HTML"
    )
    
    return await start(update, context)

async def show_all_lists(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Shows all user's lists."""
    user = update.message.from_user if update.message else update.callback_query.from_user
    user_notes = get_user_notes(user.id)
    
    message = [f"{EMOJIS['lists']} <b>Your Lists:</b>\n"]
    
    for list_type, list_name in LIST_TYPES.items():
        items = user_notes['lists'][list_type]
        if items:
            message.append(f"\n{list_name}:")
            for i, item in enumerate(items, 1):
                message.append(f"{i}. {item}")
        else:
            message.append(f"\n{list_name}: empty")
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            "\n".join(message),
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text(
            "\n".join(message),
            parse_mode="HTML",
            reply_markup=ReplyKeyboardMarkup([[f"{EMOJIS['back']} Back"]], resize_keyboard=True)
        )
    
    return LIST_CHOICE

async def prepare_delete_from_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prepares interface for item deletion."""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    user_notes = get_user_notes(user.id)
    list_type = context.user_data['current_list']
    items = user_notes['lists'][list_type]
    
    if not items:
        await query.edit_message_text(
            f"{EMOJIS['warning']} <b>This list is empty.</b>\n\n"
            f"There's nothing to remove from {LIST_TYPES[list_type]}.",
            parse_mode="HTML"
        )
        return await show_lists_menu(update, context)
    
    message = (
        f"{EMOJIS['delete']} <b>Remove Item from {LIST_TYPES[list_type]}</b>\n\n"
        "Select which item you want to remove:"
    )
    
    # Create keyboard with list items
    keyboard = []
    for i, item in enumerate(items):
        keyboard.append([InlineKeyboardButton(f"{i+1}. {item}", callback_data=f"delete_item_{i}")])
    
    keyboard.append([InlineKeyboardButton(f"{EMOJIS['back']} Back", callback_data="back")])
    
    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return DELETE_FROM_LIST

async def delete_item_from_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Deletes selected item from list."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "back":
        return await choose_list_type(update, context)
    
    # Get item index to delete
    index = int(query.data.split('_')[2])
    list_type = context.user_data['current_list']
    user_notes = get_user_notes(query.from_user.id)
    
    # Delete item
    deleted_item = user_notes['lists'][list_type].pop(index)
    
    await query.edit_message_text(
        f"{EMOJIS['done']} <b>Item removed successfully!</b>\n\n"
        f"<b>List:</b> {LIST_TYPES[list_type]}\n"
        f"<b>Removed item:</b> {deleted_item}",
        parse_mode="HTML"
    )
    
    return await start(update, context)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ends the conversation."""
    user = update.message.from_user if update.message else update.callback_query.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            "Goodbye! If you want to start again, just send /start."
        )
    else:
        await update.message.reply_text(
            "Goodbye! If you want to start again, just send /start.",
            reply_markup=ReplyKeyboardRemove()
        )

    return ConversationHandler.END

def main() -> None:
    """Runs the bot."""
    # Create Application with bot token
    application = Application.builder().token("7694434912:AAFHqjPl_AmaW7b1wQB1KjZoUrHwDbwRY_U").build()
    
    # Set up ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(filters.Regex(f"^{EMOJIS['add']} Add Note$"), add_record),
                MessageHandler(filters.Regex(f"^{EMOJIS['delete']} Delete Note$"), delete_record),
                MessageHandler(filters.Regex(f"^{EMOJIS['edit']} Edit Note$"), add_record),
                MessageHandler(filters.Regex(f"^{EMOJIS['list']} View Notes$"), list_records),
                MessageHandler(filters.Regex(f"^{EMOJIS['categories']} Categories$"), list_records),
                MessageHandler(filters.Regex(f"^{EMOJIS['lists']} My Lists$"), show_lists_menu),
                MessageHandler(filters.Regex(f"^{EMOJIS['time']} Reminders$"), set_reminder),
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_reminder_time),
            ],
            ADD_RECORD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_record),
            ],
            SELECT_CATEGORY: [
                CallbackQueryHandler(category_selected, pattern="^category_"),
                CallbackQueryHandler(category_selected, pattern="^back$"),
            ],
            DELETE_RECORD: [
                CallbackQueryHandler(delete_record_confirm),
            ],
            LIST_CHOICE: [
                MessageHandler(filters.Regex(f"^{EMOJIS['add']} Add to List$"), choose_list_action),
                MessageHandler(filters.Regex(f"^{EMOJIS['list']} View Lists$"), choose_list_action),
                MessageHandler(filters.Regex(f"^{EMOJIS['delete']} Remove from List$"), choose_list_action),
                MessageHandler(filters.Regex(f"^{EMOJIS['back']} Back$"), start),
            ],
            ADD_TO_LIST: [
                CallbackQueryHandler(list_type_selected, pattern="^list_"),
                CallbackQueryHandler(prepare_delete_from_list, pattern="^back$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_to_list),
            ],
            DELETE_FROM_LIST: [
                CallbackQueryHandler(delete_item_from_list, pattern="^delete_item_"),
                CallbackQueryHandler(choose_list_type, pattern="^back$"),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    application.add_handler(conv_handler)
    
    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()