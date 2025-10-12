import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import sqlite3
from datetime import datetime, timedelta
import aiohttp
import io
import asyncio  # Добавлен импорт asyncio
import random
from PIL import Image, ImageDraw, ImageFont

# Initialize
load_dotenv()
TOKEN = os.getenv('MTM5MDI5MzI0NTUyMjYwODE5OQ.GbycCq.BwkZDwhiIm62YHflsYBbJU7u9NLhspMEYvwUU8')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Database setup
def init_db():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY,
                  exp INTEGER DEFAULT 0,
                  voice_time INTEGER DEFAULT 0,
                  join_date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Color constants
COLORS = {
    "ban": 0xff0000,
    "kick": 0xff9900,
    "mute": 0x666666,
    "info": 0x3498db,
    "success": 0x2ecc71,
    "welcome": 0x9b59b6
}

# Helper function for beautiful embeds
def create_embed(title, description, color_name="info"):
    embed = discord.Embed(
        title=title,
        description=description,
        color=COLORS.get(color_name, 0x3498db),
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text=f"{bot.user.name} • {datetime.utcnow().strftime('%Y-%m-%d')}")
    return embed

# Welcome image generator
async def generate_welcome_image(member):
    # Create blank image
    img = Image.new('RGB', (800, 300), color=(54, 57, 63))
    draw = ImageDraw.Draw(img)
    
    # Load fonts (you'll need to provide font files)
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 40)
        text_font = ImageFont.truetype("arial.ttf", 30)
    except:
        # Fallback fonts
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Download member avatar
    async with aiohttp.ClientSession() as session:
        async with session.get(str(member.avatar.url)) as resp:
            avatar_data = await resp.read()
    
    avatar = Image.open(io.BytesIO(avatar_data)).resize((200, 200))
    
    # Create circular mask for avatar
    mask = Image.new('L', (200, 200), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, 200, 200), fill=255)
    
    # Paste avatar
    img.paste(avatar, (50, 50), mask)
    
    # Draw text
    draw.text((300, 80), f"Welcome {member.name}!", font=title_font, fill=(255, 255, 255))
    draw.text((300, 150), f"Member #{len(list(member.guild.members))}", font=text_font, fill=(200, 200, 200))
    draw.text((300, 200), f"Enjoy your stay!", font=text_font, fill=(200, 200, 200))
    
    # Save to bytes
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

# Moderation commands
@bot.tree.command(name="ban", description="Ban a user from the server")
@app_commands.describe(user="User to ban", reason="Reason for ban")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
    await user.ban(reason=reason)
    embed = create_embed(
        "🔨 User Banned",
        f"{user.mention} has been banned from the server",
        "ban"
    )
    embed.add_field(name="Reason", value=reason)
    embed.add_field(name="Moderator", value=interaction.user.mention)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="kick", description="Kick a user from the server")
@app_commands.describe(user="User to kick", reason="Reason for kick")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
    await user.kick(reason=reason)
    embed = create_embed(
        "👢 User Kicked",
        f"{user.mention} has been kicked from the server",
        "kick"
    )
    embed.add_field(name="Reason", value=reason)
    embed.add_field(name="Moderator", value=interaction.user.mention)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mute", description="Mute a user")
@app_commands.describe(user="User to mute", duration="Mute duration (e.g. 1h, 30m)", reason="Reason for mute")
@app_commands.checks.has_permissions(manage_roles=True)
async def mute(interaction: discord.Interaction, user: discord.Member, duration: str, reason: str = "No reason provided"):
    # Convert duration to seconds
    units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    try:
        amount = int(duration[:-1])
        unit = duration[-1].lower()
        seconds = amount * units[unit]
    except:
        await interaction.response.send_message("Invalid duration format! Use: 1h, 30m, 2d", ephemeral=True)
        return
    
    # Find or create muted role
    muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await interaction.guild.create_role(name="Muted")
        for channel in interaction.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)
    
    await user.add_roles(muted_role)
    
    embed = create_embed(
        "🔇 User Muted",
        f"{user.mention} has been muted for {duration}",
        "mute"
    )
    embed.add_field(name="Reason", value=reason)
    embed.add_field(name="Moderator", value=interaction.user.mention)
    await interaction.response.send_message(embed=embed)
    
    # Schedule unmute
    await asyncio.sleep(seconds)
    if muted_role in user.roles:
        await user.remove_roles(muted_role)
        await interaction.followup.send(f"{user.mention} has been automatically unmuted after {duration}")

@bot.tree.command(name="unmute", description="Unmute a user")
@app_commands.describe(user="User to unmute")
@app_commands.checks.has_permissions(manage_roles=True)
async def unmute(interaction: discord.Interaction, user: discord.Member):
    muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
    if muted_role and muted_role in user.roles:
        await user.remove_roles(muted_role)
        embed = create_embed(
            "🔊 User Unmuted",
            f"{user.mention} has been unmuted",
            "success"
        )
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("This user is not muted", ephemeral=True)

@bot.tree.command(name="unban", description="Unban a user")
@app_commands.describe(user_id="User ID to unban", reason="Reason for unban")
@app_commands.checks.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, user_id: str, reason: str = "No reason provided"):
    try:
        user = await bot.fetch_user(int(user_id))
        await interaction.guild.unban(user, reason=reason)
        embed = create_embed(
            "✅ User Unbanned",
            f"{user.mention} has been unbanned from the server",
            "success"
        )
        embed.add_field(name="Reason", value=reason)
        await interaction.response.send_message(embed=embed)
    except:
        await interaction.response.send_message("Invalid user ID or user not banned", ephemeral=True)

@bot.tree.command(name="clear", description="Clear messages")
@app_commands.describe(amount="Number of messages to clear (1-100)")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100] = 10):
    await interaction.channel.purge(limit=amount + 1)
    embed = create_embed(
        "🧹 Messages Cleared",
        f"{amount} messages have been deleted",
        "success"
    )
    msg = await interaction.channel.send(embed=embed)
    await asyncio.sleep(5)
    await msg.delete()

# Info commands
@bot.tree.command(name="serverinfo", description="Show server information")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    online = len([m for m in guild.members if m.status != discord.Status.offline])
    
    embed = create_embed(
        f"ℹ️ {guild.name} Info",
        f"Server created: {guild.created_at.strftime('%Y-%m-%d')}",
        "info"
    )
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.add_field(name="Owner", value=guild.owner.mention)
    embed.add_field(name="Members", value=f"{online} online\n{guild.member_count} total")
    embed.add_field(name="Channels", value=f"{len(guild.text_channels)} text\n{len(guild.voice_channels)} voice")
    embed.add_field(name="Roles", value=len(guild.roles))
    embed.add_field(name="Boost Level", value=guild.premium_tier)
    embed.add_field(name="Boosts", value=guild.premium_subscription_count)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="serveravatar", description="Show server avatar")
async def serveravatar(interaction: discord.Interaction):
    if interaction.guild.icon:
        embed = create_embed(
            f"{interaction.guild.name}'s Avatar",
            "",
            "info"
        )
        embed.set_image(url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("This server has no avatar", ephemeral=True)

@bot.tree.command(name="avatar", description="Show user avatar")
@app_commands.describe(user="User to show avatar for")
async def avatar(interaction: discord.Interaction, user: discord.Member = None):
    user = user or interaction.user
    embed = create_embed(
        f"{user.name}'s Avatar",
        "",
        "info"
    )
    embed.set_image(url=user.avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="exp", description="Show user experience")
@app_commands.describe(user="User to check experience for")
async def exp(interaction: discord.Interaction, user: discord.Member = None):  # Исправлена опечатка в имени параметра
    user = user or interaction.user
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("SELECT exp, voice_time FROM users WHERE user_id = ?", (user.id,))
    result = c.fetchone() or (0, 0)
    conn.close()
    
    embed = create_embed(
        f"📊 {user.name}'s Stats",
        "",
        "info"
    )
    embed.add_field(name="Total EXP", value=result[0])
    embed.add_field(name="Voice Time", value=f"{result[1] // 3600}h {(result[1] % 3600) // 60}m")
    embed.set_thumbnail(url=user.avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description="Show all commands")
async def help(interaction: discord.Interaction):
    embed = create_embed(
        "📚 Help Menu",
        "Here are all available commands:",
        "info"
    )
    
    categories = {
        "🛡️ Moderation": [
            "/ban - Ban a user",
            "/kick - Kick a user",
            "/mute - Mute a user",
            "/unmute - Unmute a user",
            "/unban - Unban a user",
            "/clear - Clear messages"
        ],
        "ℹ️ Information": [
            "/serverinfo - Server information",
            "/serveravatar - Server avatar",
            "/avatar - User avatar",
            "/exp - User experience",
            "/help - This menu"
        ]
    }
    
    for category, commands in categories.items():
        embed.add_field(
            name=category,
            value="\n".join(commands),
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)


@bot.event
async def on_member_join(member):
    # Add to database
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, join_date) VALUES (?, ?)", 
              (member.id, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    # Find welcome channel
    welcome_channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if not welcome_channel:
        welcome_channel = member.guild.system_channel
    
    if welcome_channel:
        # Generate welcome image
        image = await generate_welcome_image(member)
        file = discord.File(image, filename="welcome.png")
        
        # Send welcome message
        embed = create_embed(
            f"✨ Welcome {member.name}!",
            f"Please read the rules and enjoy your stay!\n\nAccount created: {member.created_at.strftime('%Y-%m-%d')}",
            "welcome"
        )
        embed.set_image(url="attachment://welcome.png")
        
        await welcome_channel.send(
            content=member.mention,
            embed=embed,
            file=file
        )

# Voice experience tracking
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        
        # User left voice channel
        if before.channel and not after.channel:
            c.execute("SELECT voice_time FROM users WHERE user_id = ?", (member.id,))
            result = c.fetchone()
            if result:
                time_spent = (datetime.now() - member.joined_at).seconds
                c.execute("UPDATE users SET voice_time = voice_time + ? WHERE user_id = ?", 
                         (time_spent, member.id))
                conn.commit()
        
        # User joined voice channel
        elif after.channel and not before.channel:
            c.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (member.id,))
            conn.commit()
        
        conn.close()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(f'Error syncing commands: {e}')

bot.run("MTM5MDI5MzI0NTUyMjYwODE5OQ.GbycCq.BwkZDwhiIm62YHflsYBbJU7u9NLhspMEYvwUU8")