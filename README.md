# python-programs
This file is a merged representation of the entire codebase, combined into a single document by Repomix.
The content has been processed where content has been compressed (code blocks are separated by ⋮---- delimiter), security check has been disabled.

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Content has been compressed - code blocks are separated by ⋮---- delimiter
- Security check has been disabled - content may contain sensitive information
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
2048/
  freesansbold.tff
  high_score
  main.py
  README.md
aaaemb/
  bot_stats.db
  bot.py
  moderation.db
  text
all the stars/
  main.py
apps projects/
  hentai/
    hentai/
      Assets.xcassets/
        AccentColor.colorset/
          Contents.json
        AppIcon.appiconset/
          Contents.json
        Contents.json
      hentai.entitlements
      hentaiApp.swift
    hentaiTests/
      hentaiTests.swift
    hentaiUITests/
      hentaiUITests.swift
      hentaiUITestsLaunchTests.swift
calculator python/
  main.py
CatchUnderwaterStars/
  hero.py
  main.py
  README.md
currency/
  main.py
di22vkook/
  list
  main.py
di9star/
  main.py
kittiegab/
  list
  user_data.json
main_app/
  main_app
  README.md
marwin/
  index.html
  main.py
  marwin.py
MarwinBot/
  Marwin.py
  README.md
maze/
  main.py
ping-pong/
  main.py
turtur/
  main.py
weather/
  main.py
README.md
```

# Files

## File: 2048/freesansbold.tff
```

```

## File: 2048/high_score
```
624
```

## File: 2048/main.py
```python
# initial set up
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
⋮----
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)
⋮----
# 2048 game color library
colors = {0: (204, 192, 179),
⋮----
# game variables initialize
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open('high_score', 'r')
init_high = int(file.readline())
⋮----
high_score = init_high
⋮----
# draw game over and restart text
def draw_over()
⋮----
game_over_text1 = font.render('Game Over!', True, 'white')
game_over_text2 = font.render('Press Enter to Restart', True, 'white')
⋮----
# take your turn based on direction
def take_turn(direc, board)
⋮----
merged = [[False for _ in range(4)] for _ in range(4)]
⋮----
shift = 0
⋮----
# spawn in new pieces randomly when turns start
def new_pieces(board)
⋮----
count = 0
full = False
⋮----
row = random.randint(0, 3)
col = random.randint(0, 3)
⋮----
full = True
⋮----
# draw background for the board
def draw_board()
⋮----
score_text = font.render(f'Score: {score}', True, 'black')
high_score_text = font.render(f'High Score: {high_score}', True, 'black')
⋮----
# draw tiles for game
def draw_pieces(board)
⋮----
value = board[i][j]
⋮----
value_color = colors['light text']
⋮----
value_color = colors['dark text']
⋮----
color = colors[value]
⋮----
color = colors['other']
⋮----
value_len = len(str(value))
font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
value_text = font.render(str(value), True, value_color)
text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
⋮----
# main game loop
run = True
⋮----
spawn_new = False
⋮----
board_values = take_turn(direction, board_values)
⋮----
file = open('high_score', 'w')
⋮----
init_high = high_score
⋮----
run = False
⋮----
direction = 'UP'
⋮----
direction = 'DOWN'
⋮----
direction = 'LEFT'
⋮----
direction = 'RIGHT'
⋮----
high_score = score
```

## File: 2048/README.md
```markdown
# 2048
This game is created in the likeness of the game 2048.

In it you can get the maximum number of points and develop your skills.

---

Commands:
- you can press LEFT or RIGHT and use them to move the number in the direction you want.
```

## File: aaaemb/bot.py
```python
import asyncio  # Добавлен импорт asyncio
⋮----
# Initialize
⋮----
TOKEN = os.getenv('MTM5MDI5MzI0NTUyMjYwODE5OQ.GbycCq.BwkZDwhiIm62YHflsYBbJU7u9NLhspMEYvwUU8')
⋮----
intents = discord.Intents.default()
⋮----
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
⋮----
# Database setup
def init_db()
⋮----
conn = sqlite3.connect('user_data.db')
c = conn.cursor()
⋮----
# Color constants
COLORS = {
⋮----
# Helper function for beautiful embeds
def create_embed(title, description, color_name="info")
⋮----
embed = discord.Embed(
⋮----
# Welcome image generator
async def generate_welcome_image(member)
⋮----
# Create blank image
img = Image.new('RGB', (800, 300), color=(54, 57, 63))
draw = ImageDraw.Draw(img)
⋮----
# Load fonts (you'll need to provide font files)
⋮----
title_font = ImageFont.truetype("arialbd.ttf", 40)
text_font = ImageFont.truetype("arial.ttf", 30)
⋮----
# Fallback fonts
title_font = ImageFont.load_default()
text_font = ImageFont.load_default()
⋮----
# Download member avatar
⋮----
avatar_data = await resp.read()
⋮----
avatar = Image.open(io.BytesIO(avatar_data)).resize((200, 200))
⋮----
# Create circular mask for avatar
mask = Image.new('L', (200, 200), 0)
draw_mask = ImageDraw.Draw(mask)
⋮----
# Paste avatar
⋮----
# Draw text
⋮----
# Save to bytes
buf = io.BytesIO()
⋮----
# Moderation commands
⋮----
@bot.tree.command(name="ban", description="Ban a user from the server")
@app_commands.describe(user="User to ban", reason="Reason for ban")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided")
⋮----
embed = create_embed(
⋮----
@bot.tree.command(name="kick", description="Kick a user from the server")
@app_commands.describe(user="User to kick", reason="Reason for kick")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided")
⋮----
@bot.tree.command(name="mute", description="Mute a user")
@app_commands.describe(user="User to mute", duration="Mute duration (e.g. 1h, 30m)", reason="Reason for mute")
@app_commands.checks.has_permissions(manage_roles=True)
async def mute(interaction: discord.Interaction, user: discord.Member, duration: str, reason: str = "No reason provided")
⋮----
# Convert duration to seconds
units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
⋮----
amount = int(duration[:-1])
unit = duration[-1].lower()
seconds = amount * units[unit]
⋮----
# Find or create muted role
muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
⋮----
muted_role = await interaction.guild.create_role(name="Muted")
⋮----
# Schedule unmute
⋮----
@bot.tree.command(name="unmute", description="Unmute a user")
@app_commands.describe(user="User to unmute")
@app_commands.checks.has_permissions(manage_roles=True)
async def unmute(interaction: discord.Interaction, user: discord.Member)
⋮----
@bot.tree.command(name="unban", description="Unban a user")
@app_commands.describe(user_id="User ID to unban", reason="Reason for unban")
@app_commands.checks.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, user_id: str, reason: str = "No reason provided")
⋮----
user = await bot.fetch_user(int(user_id))
⋮----
@bot.tree.command(name="clear", description="Clear messages")
@app_commands.describe(amount="Number of messages to clear (1-100)")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100] = 10)
⋮----
msg = await interaction.channel.send(embed=embed)
⋮----
# Info commands
⋮----
@bot.tree.command(name="serverinfo", description="Show server information")
async def serverinfo(interaction: discord.Interaction)
⋮----
guild = interaction.guild
online = len([m for m in guild.members if m.status != discord.Status.offline])
⋮----
@bot.tree.command(name="serveravatar", description="Show server avatar")
async def serveravatar(interaction: discord.Interaction)
⋮----
@bot.tree.command(name="avatar", description="Show user avatar")
@app_commands.describe(user="User to show avatar for")
async def avatar(interaction: discord.Interaction, user: discord.Member = None)
⋮----
user = user or interaction.user
⋮----
@bot.tree.command(name="exp", description="Show user experience")
@app_commands.describe(user="User to check experience for")
async def exp(interaction: discord.Interaction, user: discord.Member = None):  # Исправлена опечатка в имени параметра
⋮----
result = c.fetchone() or (0, 0)
⋮----
@bot.tree.command(name="help", description="Show all commands")
async def help(interaction: discord.Interaction)
⋮----
categories = {
⋮----
@bot.event
async def on_member_join(member)
⋮----
# Add to database
⋮----
# Find welcome channel
welcome_channel = discord.utils.get(member.guild.text_channels, name="welcome")
⋮----
welcome_channel = member.guild.system_channel
⋮----
# Generate welcome image
image = await generate_welcome_image(member)
file = discord.File(image, filename="welcome.png")
⋮----
# Send welcome message
⋮----
# Voice experience tracking
⋮----
@bot.event
async def on_voice_state_update(member, before, after)
⋮----
# User left voice channel
⋮----
result = c.fetchone()
⋮----
time_spent = (datetime.now() - member.joined_at).seconds
⋮----
# User joined voice channel
⋮----
@bot.event
async def on_ready()
⋮----
synced = await bot.tree.sync()
```

## File: aaaemb/text
```
#MTM5MDI5MzI0NTUyMjYwODE5OQ.GbycCq.BwkZDwhiIm62YHflsYBbJU7u9NLhspMEYvwUU8

commands:
-ban
-kick
-mute
-unmute
-unban
-clear
-serverinfo(how many people how many online and etc)
-help
-serveravatar
-avatar person
-joining beautiful with picture
-exp
-level
-coins slots
-card game
```

## File: all the stars/main.py
```python
lyrics_with_timing = [
⋮----
def print_timed_lyrics(lyrics_with_timing)
⋮----
start_time = time.time()
⋮----
words = line.split()
⋮----
sleep_time = display_time - (time.time() - start_time)
```

## File: apps projects/hentai/hentai/Assets.xcassets/AccentColor.colorset/Contents.json
```json
{
  "colors" : [
    {
      "idiom" : "universal"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
```

## File: apps projects/hentai/hentai/Assets.xcassets/AppIcon.appiconset/Contents.json
```json
{
  "images" : [
    {
      "idiom" : "universal",
      "platform" : "ios",
      "size" : "1024x1024"
    },
    {
      "appearances" : [
        {
          "appearance" : "luminosity",
          "value" : "dark"
        }
      ],
      "idiom" : "universal",
      "platform" : "ios",
      "size" : "1024x1024"
    },
    {
      "appearances" : [
        {
          "appearance" : "luminosity",
          "value" : "tinted"
        }
      ],
      "idiom" : "universal",
      "platform" : "ios",
      "size" : "1024x1024"
    },
    {
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "16x16"
    },
    {
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "16x16"
    },
    {
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "32x32"
    },
    {
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "32x32"
    },
    {
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "128x128"
    },
    {
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "128x128"
    },
    {
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "256x256"
    },
    {
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "256x256"
    },
    {
      "idiom" : "mac",
      "scale" : "1x",
      "size" : "512x512"
    },
    {
      "idiom" : "mac",
      "scale" : "2x",
      "size" : "512x512"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
```

## File: apps projects/hentai/hentai/Assets.xcassets/Contents.json
```json
{
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
```

## File: apps projects/hentai/hentai/hentai.entitlements
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>
    <key>com.apple.security.files.user-selected.read-only</key>
    <true/>
</dict>
</plist>
```

## File: apps projects/hentai/hentai/hentaiApp.swift
```swift
//
//  hentaiApp.swift
//  hentai
⋮----
//  Created by di9star on 22.07.25.
⋮----
struct hentaiApp: App {
var body: some Scene {
```

## File: apps projects/hentai/hentaiTests/hentaiTests.swift
```swift
//
//  hentaiTests.swift
//  hentaiTests
⋮----
//  Created by di9star on 22.07.25.
⋮----
struct hentaiTests {
⋮----
@Test func example() async throws {
// Write your test here and use APIs like `#expect(...)` to check expected conditions.
```

## File: apps projects/hentai/hentaiUITests/hentaiUITests.swift
```swift
//
//  hentaiUITests.swift
//  hentaiUITests
⋮----
//  Created by di9star on 22.07.25.
⋮----
final class hentaiUITests: XCTestCase {
⋮----
override func setUpWithError() throws {
// Put setup code here. This method is called before the invocation of each test method in the class.
⋮----
// In UI tests it is usually best to stop immediately when a failure occurs.
⋮----
// In UI tests it’s important to set the initial state - such as interface orientation - required for your tests before they run. The setUp method is a good place to do this.
⋮----
override func tearDownWithError() throws {
// Put teardown code here. This method is called after the invocation of each test method in the class.
⋮----
func testExample() throws {
// UI tests must launch the application that they test.
let app = XCUIApplication()
⋮----
// Use XCTAssert and related functions to verify your tests produce the correct results.
⋮----
func testLaunchPerformance() throws {
// This measures how long it takes to launch your application.
```

## File: apps projects/hentai/hentaiUITests/hentaiUITestsLaunchTests.swift
```swift
//
//  hentaiUITestsLaunchTests.swift
//  hentaiUITests
⋮----
//  Created by di9star on 22.07.25.
⋮----
final class hentaiUITestsLaunchTests: XCTestCase {
⋮----
override class var runsForEachTargetApplicationUIConfiguration: Bool {
⋮----
override func setUpWithError() throws {
⋮----
func testLaunch() throws {
let app = XCUIApplication()
⋮----
// Insert steps here to perform after app launch but before taking a screenshot,
// such as logging into a test account or navigating somewhere in the app
⋮----
let attachment = XCTAttachment(screenshot: app.screenshot())
```

## File: calculator python/main.py
```python
def button_press(num)
⋮----
equation_text = equation_text + str(num)
⋮----
def equals()
⋮----
total = str(eval(equation_text))
⋮----
equation_text = total
⋮----
equation_text = ""
⋮----
def clear_calc()
⋮----
window = tk.Tk()
⋮----
equation_label = StringVar()
⋮----
label = tk.Label(window, textvariable=equation_label, font=('consolas',20),
⋮----
frame = tk.Frame(window)
⋮----
# Создаем кнопки цифр
buttons = []
⋮----
button = tk.Button(frame, text=str(i), height=4, width=9, font=35,
⋮----
# Располагаем кнопки в сетке 3x3
⋮----
button0 = tk.Button(frame, text='0', height=4, width=9, font=35,
⋮----
# Кнопки операций
operations = ['+', '-', '*', '/']
⋮----
button = tk.Button(frame, text=op, height=4, width=9, font=35,
⋮----
equal = tk.Button(frame, text='=', height=4, width=9, font=35,
⋮----
decimal = tk.Button(frame, text='.', height=4, width=9, font=35,
⋮----
clear_button = tk.Button(window, text='clear', height=4, width=12, font=35,
```

## File: CatchUnderwaterStars/hero.py
```python
class Hero
⋮----
def __init__(self, window)
⋮----
def update(self)
⋮----
keys = pygame.key.get_pressed()
```

## File: CatchUnderwaterStars/main.py
```python
window = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()
background = pygame.transform.scale(pygame.image.load('background.jpg'), (1200, 800))
hero = Hero(window)
```

## File: CatchUnderwaterStars/README.md
```markdown
В далекие времена, когда море было еще неисследованным и загадочным местом, жил один отважный дайвер по имени Александр. Он был известен своей смелостью и любовью к подводным приключениям. Все, что было связано с водой, притягивало его, и он решил отправиться в увлекательное путешествие в подводный мир.

Александр услышал о легенде, которая гласила, что в глубинах морского царства существует магический артефакт, способный исполнить любое желание своего обладателя. Чтобы найти этот артефакт, Александру нужно было собрать звезды и монеты, разбросанные по дну океана.

С сумкой для снаряжения на плече и глубиномером на запястье, Александр погрузился в таинственные глубины моря. Он встретил разнообразных морских обитателей, которые помогали ему или представляли опасность. Рыбки-помощники подсказывали ему путь к звездам, а крабы и осьминоги пытались его остановить.

Однако, ничто не могло остановить Александра в его стремлении достичь своей цели. Он плавал между коралловыми рифами, исследовал потайные пещеры и плавал среди затонувших кораблей, всегда собирая звезды и монеты на своем пути.

Но самое сложное испытание ждало его в самом глубоком месте морского царства. Там, во тьме и бездне, обитал огромный и страшный кракен, считавшийся стражем артефакта. Александру пришлось сразиться с ним, проявив всю свою смелость и силу. Сражение было ожесточенным, но Александр, собрав все свои силы, одержал победу.

Наконец, Александр достиг цели своего путешествия. Перед ним открылся величественный храм, где хранился магический артефакт.
```

## File: currency/main.py
```python
bot = telebot.TeleBot('your_bot_token')
currency = CurrencyConverter()
amount = 0
⋮----
@bot.message_handler(commands=['start'])
def start(message)
⋮----
def summa(message)
⋮----
amount = int(message.text.strip())
⋮----
markup = types.InlineKeyboardMarkup(row_width=2)
btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
btn3 = types.InlineKeyboardButton('RUB/BYN', callback_data='rub/byn')
btn4 = types.InlineKeyboardButton('BYN/RUB', callback_data='byn/rub')
btn5 = types.InlineKeyboardButton('USD/BYN', callback_data='usd/byn')
btn6 = types.InlineKeyboardButton('BYN/USD', callback_data='byn/usd')
btn7 = types.InlineKeyboardButton('KZT/BYN', callback_data='kzt/byn')
btn8 = types.InlineKeyboardButton('BYN/KZT', callback_data='byn/kzt')
btn9 = types.InlineKeyboardButton('IDR/BYN', callback_data='idr/byn')
btn10 = types.InlineKeyboardButton('BYN/IDR', callback_data='byn/idr')
btn11 = types.InlineKeyboardButton('Другое значение - Other meaning', callback_data='else')
⋮----
@bot.callback_query_handler(func = lambda call: True)
def callback(call)
⋮----
values = call.data.upper().split('/')
res = currency.convert(amount, values[0], values[1])
⋮----
def my_currency(message)
⋮----
values = message.rext.upper().split('/')
```

## File: di22vkook/list
```
#7694434912:AAFHqjPl_AmaW7b1wQB1KjZoUrHwDbwRY_U
```

## File: di22vkook/main.py
```python
# Logging setup
⋮----
logger = logging.getLogger(__name__)
⋮----
# Conversation states
⋮----
# Emojis for UI
EMOJIS = {
⋮----
# Categories with emojis
CATEGORIES = {
⋮----
# List types
LIST_TYPES = {
⋮----
# User data storage
user_data = {}
⋮----
def get_today_date()
⋮----
"""Returns today's date in DD.MM.YYYY format"""
⋮----
def get_user_notes(user_id: int)
⋮----
"""Gets or creates user's notes"""
⋮----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int
⋮----
"""Starts the conversation with main menu."""
user = update.message.from_user if update.message else update.callback_query.from_user
⋮----
welcome_message = (
⋮----
reply_keyboard = [
⋮----
async def add_record(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int
⋮----
"""Starts adding a new note."""
⋮----
message = (
⋮----
async def save_record(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int
⋮----
"""Saves the note and asks for category."""
user = update.message.from_user
text = update.message.text
user_notes = get_user_notes(user.id)
⋮----
# Save text temporarily
⋮----
# Create category keyboard
keyboard = []
⋮----
async def category_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int
⋮----
"""Handles category selection and saves note."""
query = update.callback_query
⋮----
user = query.from_user
⋮----
# Get category from callback_data (format "category_work")
category = query.data.split('_')[1]
note_text = context.user_data['temp_note']
⋮----
# Get current date
today = get_today_date()
⋮----
# Add note
⋮----
# Send new message with main menu
⋮----
async def delete_record(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int
⋮----
"""Shows notes for deletion."""
⋮----
# Create keyboard with notes
⋮----
async def delete_record_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int
⋮----
"""Deletes the selected note."""
⋮----
# Get data from callback_data (format "delete_DD.MM.YYYY_index")
⋮----
index = int(index)
⋮----
# Delete note
deleted_note = user_notes['notes'][date].pop(index)
⋮----
# Remove date if no notes left
⋮----
async def list_records(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None
⋮----
"""Shows all user's notes."""
⋮----
response = [f"{EMOJIS['notebook']} <b>Your Notes:</b>\n"]
⋮----
async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int
⋮----
"""Sets up daily reminder time."""
⋮----
async def process_reminder_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int
⋮----
"""Processes the reminder time input."""
⋮----
# Parse time
⋮----
reminder_time = time(hour, minute)
⋮----
# Save time for user
⋮----
# Remove old job if exists
current_jobs = context.job_queue.get_jobs_by_name(str(user.id))
⋮----
# Set new job in JobQueue
⋮----
async def send_daily_reminder(context: ContextTypes.DEFAULT_TYPE)
⋮----
"""Sends daily reminder with today's notes."""
job = context.job
user_id = int(job.name)
⋮----
user_notes = user_data[user_id]
⋮----
message = [f"{EMOJIS['notebook']} <b>Your Notes for Today ({today}):</b>"]
⋮----
async def show_lists_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int
⋮----
"""Shows lists management menu."""
⋮----
async def choose_list_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int
⋮----
"""Chooses list action."""
⋮----
action = update.message.text if update.message else None
⋮----
# Determine selected action
⋮----
async def choose_list_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int
⋮----
"""Chooses list type to work with."""
⋮----
# Create keyboard with list types
⋮----
async def list_type_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int
⋮----
"""Handles list type selection."""
⋮----
# Get list type from callback_data (format "list_drama")
list_type = query.data.split('_')[1]
⋮----
async def add_to_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int
⋮----
"""Adds item to selected list."""
⋮----
list_type = context.user_data['current_list']
⋮----
# Add item to list
⋮----
async def show_all_lists(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int
⋮----
"""Shows all user's lists."""
⋮----
message = [f"{EMOJIS['lists']} <b>Your Lists:</b>\n"]
⋮----
items = user_notes['lists'][list_type]
⋮----
async def prepare_delete_from_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int
⋮----
"""Prepares interface for item deletion."""
⋮----
# Create keyboard with list items
⋮----
async def delete_item_from_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int
⋮----
"""Deletes selected item from list."""
⋮----
# Get item index to delete
index = int(query.data.split('_')[2])
⋮----
user_notes = get_user_notes(query.from_user.id)
⋮----
# Delete item
deleted_item = user_notes['lists'][list_type].pop(index)
⋮----
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int
⋮----
"""Ends the conversation."""
⋮----
def main() -> None
⋮----
"""Runs the bot."""
# Create Application with bot token
application = Application.builder().token("7694434912:AAFHqjPl_AmaW7b1wQB1KjZoUrHwDbwRY_U").build()
⋮----
# Set up ConversationHandler
conv_handler = ConversationHandler(
⋮----
# Run the bot
```

## File: di9star/main.py
```python
# Настройка логгирования
⋮----
logger = logging.getLogger(__name__)
⋮----
# Данные пользователя (временное хранилище)
user_data = defaultdict(lambda: {
⋮----
# Клавиатура основного меню
main_keyboard = ReplyKeyboardMarkup(
⋮----
# Все возможные вкусы мороженого
FLAVORS = {
⋮----
RARITY_WEIGHTS = {
⋮----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None
⋮----
"""Обработка команды /start."""
user = update.message.from_user
⋮----
# Проверяем, можно ли выдать мороженое
⋮----
async def check_ice_cream_drop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None
⋮----
"""Проверяет, можно ли выдать мороженое пользователю."""
user_id = update.effective_user.id
now = datetime.now()
⋮----
# Первый раз - выдаем сразу
⋮----
last_drop = user_data[user_id]["last_drop"]
⋮----
next_drop = last_drop + timedelta(hours=3)
wait_time = next_drop - now
hours = wait_time.seconds // 3600
minutes = (wait_time.seconds % 3600) // 60
⋮----
async def drop_random_flavor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None
⋮----
"""Выдает случайный вкус мороженого."""
⋮----
# Выбираем случайный вкус с учетом редкости
flavors_by_rarity = {}
⋮----
# Взвешенный случайный выбор редкости
chosen_rarity = random.choices(
⋮----
# Выбираем случайный вкус выбранной редкости
chosen_flavor = random.choice(flavors_by_rarity[chosen_rarity])
flavor_data = FLAVORS[chosen_flavor]
⋮----
# Обновляем данные пользователя
⋮----
# Определяем сообщение в зависимости от редкости
rarity_messages = {
⋮----
# Отправляем сообщение
⋮----
async def show_collection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None
⋮----
"""Показывает коллекцию мороженого пользователя."""
⋮----
collection = user_data[user_id]["collection"]
⋮----
# Группируем по редкости
⋮----
rarity = FLAVORS[flavor]["rarity"]
⋮----
# Сортируем по редкости (от легендарных к обычным)
sorted_rarities = sorted(flavors_by_rarity.items(),
⋮----
# Формируем сообщение
message = ["<b>🍨 Your ice cream collection:</b>\n"]
⋮----
emoji = FLAVORS[flavor]["emoji"]
⋮----
# Статистика
total_flavors = sum(collection.values())
unique_flavors = len(collection)
percentage = (unique_flavors / len(FLAVORS)) * 100
⋮----
# Прогресс бар коллекции
progress = int((unique_flavors / len(FLAVORS)) * 20)
⋮----
keyboard = InlineKeyboardMarkup([
⋮----
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None
⋮----
"""Красиво оформленный профиль со статистикой мороженого."""
⋮----
total_ice_cream = user_data[user_id]["ice_cream_count"]
unique_flavors = len(user_data[user_id]["collection"])
⋮----
# Генерация графика мороженого
ice_cream_chart = generate_ice_cream_chart(user_data[user_id])
⋮----
profile_text = f"""
⋮----
photo_url = "https://via.placeholder.com/400x300?text=Developer+Photo"
⋮----
def generate_ice_cream_chart(user_data)
⋮----
"""Генерация графика потребления мороженого."""
⋮----
total = sum(user_data["flavors"].values())
chart = []
⋮----
# Сортируем по количеству
sorted_flavors = sorted(user_data["flavors"].items(), key=lambda x: x[1], reverse=True)
⋮----
for flavor, count in sorted_flavors[:5]:  # Показываем топ-5
emoji = FLAVORS.get(flavor, {}).get("emoji", "🍦")
percentage = (count / total) * 100
bar = "⬛" * int(percentage / 10)
⋮----
async def social_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None
⋮----
"""Social media."""
⋮----
async def projects(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None
⋮----
"""Projects with links on GitHub."""
projects_text = """
⋮----
async def ice_cream_counter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None
⋮----
"""Счетчик мороженого с красивой таблицей."""
⋮----
today = datetime.now().strftime("%Y-%m-%d")
⋮----
# Инициализация данных
⋮----
stats_text = generate_ice_cream_stats(user_data[user_id])
⋮----
def generate_ice_cream_stats(user_data)
⋮----
"""Генерация красивой таблицы статистики."""
⋮----
total = user_data["ice_cream_count"]
today_count = user_data["dates"].get(today, 0)
week_count = sum(user_data["dates"].get((datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"), 0)
⋮----
# Красивая таблица с псевдографикой
table = [
⋮----
# Топ-3 вкуса
⋮----
top_flavors = sorted(user_data["flavors"].items(), key=lambda x: x[1], reverse=True)[:3]
⋮----
def generate_detailed_stats(user_data)
⋮----
"""Генерация детальной статистики."""
⋮----
# Статистика по дням
days_stats = []
⋮----
date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
count = user_data["dates"].get(date, 0)
⋮----
# Статистика по вкусам
flavors_stats = sorted(user_data["flavors"].items(), key=lambda x: x[1], reverse=True)
⋮----
message = [
⋮----
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None
⋮----
"""Обработка нажатий на inline-кнопки."""
query = update.callback_query
user_id = query.from_user.id
data = query.data
⋮----
flavor = data.split("_")[1]
⋮----
# Обновляем счетчики
⋮----
detailed_stats = generate_detailed_stats(user_data[user_id])
⋮----
# Добавляем последний полученный вкус в статистику
⋮----
last_flavor = max(user_data[user_id]["collection"].items(), key=lambda x: x[1])[0]
⋮----
# Обновляем сообщение
⋮----
async def show_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None
⋮----
"""List of commands."""
text = """
⋮----
def main() -> None
⋮----
"""Запуск бота."""
application = Application.builder().token("7229958377:AAHBaIbaHo7sHhudrtZDbHgBpiZCTUzTnkI").build()
⋮----
# Обработчики команд
⋮----
# Обработчики сообщений (кнопки)
⋮----
# Обработчик inline-кнопок
⋮----
# Запуск бота
```

## File: kittiegab/list
```
Валюта: 🥛| 🎟 |💎
Персонажи: 😺|😸|😹|😻

Геймплей:
    Система баланса
    Транзакции между игроками

Система уровней и опыта:
    Топы (🥇🥈🥉) 
    Баффы (🐟🐠🐡🍗🥩🍖🍤🥓)

Магазин:
    Покупка (💎🎟) | (🐟🐠🐡🍗🥩🍖🍤🥓)

Профиль:
    Статистика (уровень|баланс|дни|предметы|стрики|таймер наград|достижения)
    Темы профиля
    Коллекции (карточки|персонажи)

Дейлики:
    Награды (🥛| 🎟 )
    Стрик (🔥)
    Игры на (🥛)
    Рулетка | Казино | Кликкер | Колесо фортуны

Меню:
    Main message(со всеми командами)

Ава:
    котик, молочко, слоты и тд.

#7933175895:AAHp3rloDWy6X3m5lsV9bIanTaGO159GwYk
```

## File: kittiegab/user_data.json
```json
{"1491362479": {"balance": 1362, "fish": {}, "pets": [], "inventory": ["aquarium", "castle"], "level": 1, "xp": 0, "last_daily": "2025-05-26T07:37:29.818848", "slots_played": 0, "slots_won": 0, "wheel_spins": 4, "achievements": []}}
```

## File: main_app/main_app
```
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from instructions import txt_instruction, txt_test1, txt_test2, txt_test3, txt_sits
from ruffier import test
from seconds import Seconds


age = 7
name = ""
p1, p2, p3 = 0, 0, 0

def check_in(str_num):
    try:
        return int(str_num)
    except:
        return False


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        txt = Label(text = txt_instruction)
        txt_name = Label(text = 'Введите имя:')
        txt_age = Label(text = 'Введите возраст:')
        self.name_input = TextInput(text = '...', multiline = False)
        self.age_input = TextInput(text = '7', multiline = False)
        self.btn = Button(text = 'Start', size_hint = (0.3, 0.1), pos_hint = {'center_x':0.5})
        hl1 = BoxLayout(height = '30sp', size_hint = (0.8, None))
        hl2 = BoxLayout(height = '30sp', size_hint = (0.8, None))
        hl1.add_widget(txt_name)
        hl1.add_widget(self.name_input)
        hl2.add_widget(txt_age)
        hl2.add_widget(self.age_input)
        ml = BoxLayout(orientation = 'vertical', padding = 10, spacing = 10)
        ml.add_widget(txt)
        ml.add_widget(hl1)
        ml.add_widget(hl2)
        ml.add_widget(self.btn)
        self.btn.on_press = self.next
        self.add_widget(ml)

    def next(self):
        global name, age
        name = self.name_input.text
        age = check_in(self.age_input.text)
        if age == False or age < 7:
            age = 7
            self.age_input.text = str(age)
        else:
            self.manager.current = 'First'


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sec = Seconds(1)
        self.sec.bind(done = self.enable_sec)
        self.next_screen = False
        txt = Label(text = txt_test1)
        txt_result = Label(text = 'Введите результат:')
        self.name_result = TextInput(text = '0', multiline = False)
        self.btn = Button(text = 'Начать замер', size_hint = (0.3, 0.1), pos_hint = {'center_x':0.5})
        hl3 = BoxLayout(height = '30sp', size_hint = (0.8, None))
        hl3.add_widget(txt_result)
        hl3.add_widget(self.name_result)
        ml2 = BoxLayout(orientation = 'vertical', padding = 10, spacing = 10)
        ml2.add_widget(txt)
        ml2.add_widget(hl3)
        ml2.add_widget(self.sec)
        ml2.add_widget(self.btn)
        self.btn.on_press = self.next_sec
        self.add_widget(ml2)

    def enable_sec(self, *args):
        self.btn.set_disabled(False)
        self.name_result.set_disabled(False)
        self.next_screen = True
        self.btn.text = 'Continue'

    def next_sec(self):
        global p1
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.name_result.set_disabled(True)
            self.sec.start()
        else:
            p1 = check_in(self.name_result.text)
            if p1 == False or p1 < 1:
                p1 = 0
                self.name_result.text = str(p1)
            else:
                pass
            self.manager.current = 'Second'
        

class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.second = Seconds(1)
        self.second.bind(done = self.only_sec)
        self.second_screen = False
        txt = Label(text = txt_sits)
        self.btn = Button(text = 'Continue', size_hint = (0.3, 0.1), pos_hint = {'center_x':0.5})
        hl4 = BoxLayout(height = '30sp', size_hint = (0.8, None))
        ml3 = BoxLayout(orientation = 'vertical', padding = 10, spacing = 10)
        ml3.add_widget(txt)
        ml3.add_widget(hl4)
        ml3.add_widget(self.second)
        ml3.add_widget(self.btn)
        self.btn.on_press = self.next_sec
        self.add_widget(ml3)

    def only_sec(self, *args):
        self.btn.set_disabled(False)
        self.second_screen = True
        self.btn.text = 'Continue'

    def next_sec(self):
        if not self.second_screen:
            self.btn.set_disabled(True)
            self.second.start()
        else:
            self.manager.current = 'Third'


class FourthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.seconds = Seconds(1)
        self.seconds.bind(done = self.just_sec)
        self.third_screen = False
        txt = Label(text = txt_test3)
        txt_name = Label(text = 'Результат:')
        txt_age = Label(text = 'Результат после отдыха:')
        self.name_next = TextInput(text = '0', multiline = False)
        self.age_next = TextInput(text = '0', multiline = False)
        self.btn = Button(text = 'Continue', size_hint = (0.3, 0.1), pos_hint = {'center_x':0.5})
        hl5 = BoxLayout(height = '30sp', size_hint = (0.8, None))
        hl6 = BoxLayout(height = '30sp', size_hint = (0.8, None))
        hl5.add_widget(txt_name)
        hl5.add_widget(self.name_next)
        hl6.add_widget(txt_age)
        hl6.add_widget(self.age_next)
        ml4 = BoxLayout(orientation = 'vertical', padding = 10, spacing = 10)
        ml4.add_widget(txt)
        ml4.add_widget(hl5)
        ml4.add_widget(hl6)
        ml4.add_widget(self.seconds)
        ml4.add_widget(self.btn)
        self.btn.on_press = self.next
        self.add_widget(ml4)
    
    def just_sec(self, *args):
        self.btn.set_disabled(False)
        self.name_next.set_disabled(False)
        self.third_screen = True
        self.btn.text = 'Continue'

    def next(self):
        global p2, p3
        p2 = check_in(self.name_next.text)
        p3 = check_in(self.age_next.text)
        if (p3 == False or p3 < 0) and (p2 == False or p2 < 0):
            print((p3 == False or p3 < 0) and (p2 == False or p2 < 0))
            p3 = 0
            p2 = 0
            self.name_next.text = str(p3)            
            self.age_next.text = str(p2)            
        else:
            self.manager.current = 'Last'


class FifthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        hl7 = BoxLayout(orientation = 'vertical')
        self.str = Label(text = '')
        hl7.add_widget(self.str)
        self.add_widget(hl7)
        self.on_enter = self.before

    def before(self):
        global name
        self.str.text = name + '\n' + test(p1, p2, p3, age)


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name = 'Main'))
        sm.add_widget(SecondScreen(name = 'First'))
        sm.add_widget(ThirdScreen(name = 'Second'))
        sm.add_widget(FourthScreen(name = 'Third'))
        sm.add_widget(FifthScreen(name = 'Last'))
        return sm

app = MyApp()
app.run()
```

## File: main_app/README.md
```markdown
underwater game
```

## File: marwin/index.html
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=advice-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Shop</title>
</head>
<body>
    <div id="main">
        <h1>Онлайн магазин</h1>
        <img src="">
        <p>Loren inpun dolor sit amet, ncbdsjkfjvbvbhjaerfvrhjfh.</p>
        <button id="buy">Купить</button>
    </div>
</body>

</html>
```

## File: marwin/main.py
```python
bot = Bot('')
dp = Dispatcher(bot)
⋮----
async def start(message: types.Message)
⋮----
markup = types.ReplyKeyboardMarkup()
```

## File: marwin/marwin.py
```python
bot = Bot('')
dp = Dispatcher(bot)
⋮----
@dp.message_handler(content_types=['photo'])
async def start(message: types.Message)
⋮----
@dp.message_handler()
async def info(message: types.Message)
⋮----
markup = types.InlineKeyboardMarkup()
⋮----
@dp.callback_query_handler(commands=['inline'])
async def callback(call)
⋮----
@dp.message_handler(commands=['reply'])
async def reply(message: types.Message)
⋮----
markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
```

## File: MarwinBot/Marwin.py
```python
bot = Bot('6322621773:AAHPcJkJwLFS_jpzWWhOJPbMtjiW261huMo')
dp = Dispatcher(bot)
⋮----
@dp.message_handler(commands=['start'])
async def start(message: types.Message)
⋮----
@dp.message_handler()
async def info(message: types.Message)
⋮----
markup = types.InlineKeyboardMarkup()
⋮----
@dp.callback_query_handler()
async def callback(call)
⋮----
@dp.message_handler(commands=['reply'])
async def reply(message: types.Message)
⋮----
markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
```

## File: MarwinBot/README.md
```markdown
Некогда в маленьком городке жила одна семья, у которой было двое детей: старшая дочь Марина и младший сын Максим. Эти дети всегда были очень близки и любили проводить время вместе, особенно когда дело касалось игрушек.

Однажды, в день рождения Максима, Марина решила подарить ему что-то особенное. Она долго думала, какую игрушку ей выбрать, чтобы она была не только интересной, но и развивающей. Так она и услышала о магазине Marwin, который специализировался на игрушках для детей всех возрастов.

В этот же день Марина отправилась в магазин Marwin, чтобы найти идеальный подарок для Максима. Когда она вошла, ее встретил чат-бот магазина. Он был дружелюбный и улыбался, а его голос звучал мягко и приятно.

"Добро пожаловать в магазин Marwin! Чем я могу вам помочь?" - спросил чат-бот.

Марина рассказала ему о своей задаче - найти игрушку для Максима, которая была бы интересной и развивающей. Чат-бот внимательно слушал и с радостью предложил ей несколько вариантов.

"У нас есть широкий ассортимент игрушек для детей всех возрастов. Для вашего братика, я рекомендую взглянуть на наши конструкторы, которые помогут развивать его логическое мышление и творческие навыки. Они также очень интересны для детей от 1-18 лет", - сказал чат-бот.

Марина была впечатлена знаниями чат-бота о продуктах магазина и решила следовать его совету. Она выбрала набор конструктора, который позволял создавать разные модели, от простых до сложных. Это было идеальное решение, ведь Максим любил экспериментировать и создавать что-то новое.

Когда Марина вернулась домой, она встретила Максима с подарком. Он был в восторге от нового конструктора и сразу приступил к его сборке.
```

## File: maze/main.py
```python
money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')
⋮----
font = font.SysFont('Arial', 40)
win = font.render('YOU WIN!', True, (224, 217, 180))
lose = font.render('YOU LOSE!', True, (116, 183, 211))
⋮----
class GameSprite(sprite.Sprite)
⋮----
def __init__(self, player_image, player_x, player_y, player_speed)
def reset(self)
⋮----
class Player(GameSprite)
⋮----
def update(self)
⋮----
keys = key.get_pressed()
⋮----
class Enemy(GameSprite)
⋮----
direction = 'left'
⋮----
class Kill(GameSprite)
⋮----
class Wall(sprite.Sprite)
⋮----
def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height)
def draw_wall(self)
⋮----
win_width = 900
win_height = 700
window = display.set_mode((win_width, win_height))
⋮----
background = transform.scale(image.load('ajy.jpg'), (win_width, win_height))
⋮----
player = Player('hero.png', 5, win_height - 700, 4)
cyborg = Enemy('cyborg.png', 800, win_height - 600, 3)
treasure = GameSprite('treasure.png', 800, win_height - 100, 2)
knife = Kill('knife.png', 5, win_height - 100, 4)
⋮----
w1 = Wall(201,234,205, 90, 10, 550, 10)
w2 = Wall(201,234,205, 100, 650, 650, 10)
w3 = Wall(201,234,205, 300, 10, 10, 550)
w4 = Wall(201,234,205, 90, 20, 10, 500)
w5 = Wall(201,234,205, 500, 100, 10, 550)
⋮----
clock = time.Clock()
⋮----
game = True
⋮----
finish = False
⋮----
game = False
⋮----
finish = True
```

## File: ping-pong/main.py
```python
window = pygame.display.set_mode((700, 700))
bg = pygame.transform.scale(pygame.image.load('fon.jpg'), (700, 700))
clock = pygame.time.Clock()
⋮----
font1 = pygame.font.SysFont('Arial', 60)
⋮----
class GameSprite(pygame.sprite.Sprite)
⋮----
def __init__(self, image, x, y, w, h, speed)
⋮----
def reset(self)
⋮----
class Player(GameSprite)
⋮----
def update_l(self)
⋮----
keys = pygame.key.get_pressed()
⋮----
def update_r(self)
⋮----
rocket1 = Player('racket.png', 10, 200, 50, 150, 4)
rocket2 = Player('racket.png', 640, 200, 50, 150, 4)
ball = GameSprite('tenis_ball.png', 320, 320, 50, 50, 4)
⋮----
speed_x = 3
speed_y = 3
⋮----
finish = False
⋮----
finish = True
```

## File: turtur/main.py
```python
# Настройка логирования
⋮----
logger = logging.getLogger(__name__)
⋮----
# Файлы для хранения данных
DATA_FILE = 'turtle_data.json'
LEADERBOARD_FILE = 'leaderboard.json'
⋮----
# Загрузка данных
def load_data()
⋮----
def load_leaderboard()
⋮----
user_data = load_data()
leaderboard = load_leaderboard()
⋮----
# Магазин предметов
SHOP_ITEMS = {
⋮----
# Сохранение данных
def save_data()
⋮----
# Инициализация черепашки
def init_turtle(user_id, username)
⋮----
# Обновление лидерборда
def update_leaderboard(user_id, username, level)
⋮----
# Проверка повышения уровня
def check_level_up(user_id)
⋮----
turtle = user_data[str(user_id)]
exp_needed = turtle['level'] * 10
⋮----
# Клавиатуры
def main_menu_keyboard()
⋮----
buttons = [
⋮----
def back_keyboard(target='back')
⋮----
# Команды бота
def start(update: Update, context: CallbackContext) -> None
⋮----
user = update.effective_user
username = user.username or user.first_name
⋮----
def show_status(update: Update, context: CallbackContext) -> None
⋮----
user_id = update.effective_user.id
⋮----
message = (
⋮----
def help_command(update: Update, context: CallbackContext) -> None
⋮----
# Обработчики действий
def feed_menu(update: Update, context: CallbackContext) -> None
⋮----
user_id = update.callback_query.from_user.id
⋮----
buttons = []
⋮----
def use_item(update: Update, context: CallbackContext, item: str) -> None
⋮----
effects = SHOP_ITEMS[item]
⋮----
def play_with_turtle(update: Update, context: CallbackContext) -> None
⋮----
now = datetime.now()
last_played = datetime.fromisoformat(turtle['last_played']) if turtle['last_played'] else None
⋮----
next_play = last_played + timedelta(hours=1)
wait_time = next_play - now
hours = wait_time.seconds // 3600
minutes = (wait_time.seconds % 3600) // 60
⋮----
happiness_gain = random.randint(5, 15)
⋮----
def show_shop(update: Update, context: CallbackContext) -> None
⋮----
def buy_item(update: Update, context: CallbackContext, item: str) -> None
⋮----
item_data = SHOP_ITEMS[item]
⋮----
def heal_turtle(update: Update, context: CallbackContext) -> None
⋮----
health_gain = SHOP_ITEMS['medicine']['health']
⋮----
def show_leaderboard(update: Update, context: CallbackContext) -> None
⋮----
text = "🏆 Топ 10 игроков:\n\n"
⋮----
def rename_turtle(update: Update, context: CallbackContext) -> None
⋮----
def process_name(update: Update, context: CallbackContext) -> None
⋮----
new_name = update.message.text.strip()[:20]
⋮----
def daily_reward(update: Update, context: CallbackContext) -> None
⋮----
last_daily = datetime.fromisoformat(turtle['last_daily']) if turtle['last_daily'] else None
⋮----
reward = random.randint(10, 30)
⋮----
next_daily = last_daily + timedelta(days=1)
wait_time = next_daily - now
⋮----
# Обработчик кнопок
def button_handler(update: Update, context: CallbackContext) -> None
⋮----
query = update.callback_query
⋮----
data = query.data
⋮----
# Обработчик сообщений
def message_handler(update: Update, context: CallbackContext) -> None
⋮----
# Ошибки
def error_handler(update: Update, context: CallbackContext) -> None
⋮----
# Запуск бота
def main()
⋮----
TOKEN = "7546017621:AAGDDQMf4s0XeloeSiMXOqOeJIPk2QnuaCU"  # Замените на ваш токен
⋮----
updater = Updater(TOKEN)
dp = updater.dispatcher
⋮----
# Команды
⋮----
# Обработчики
```

## File: weather/main.py
```python
bot = telebot.TeleBot('your_bot_token')
API = 'api'
⋮----
@bot.message_handler(commands=['start'])
def start(message)
⋮----
@bot.message_handler(content_types=['text'])
def get_weather(message)
⋮----
city = message.text.strip().lower()
res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
data = json.loads(res.text)
temp = data["main"]["temp"]
⋮----
image = 'sun.png' if temp > 10.0 else 'bubbles.png'
file = open('./' + image, 'rb')
```

## File: README.md
```markdown
# python-programs
```
