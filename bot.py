import discord
from discord.ext import commands
import asyncio
import os

TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    print("Error: DISCORD_TOKEN environment variable not set.")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

pomodoro_running = False
pomodoro_message = None
remaining_time = 0
is_paused = False

async def update_timer_message(channel, seconds):
    global pomodoro_message
    minutes, secs = divmod(seconds, 60)
    time_string = f"{minutes:02}:{secs:02}"
    if pomodoro_message:
        await pomodoro_message.edit(content=f"☕ Pomodoro Timer: {time_string} {'(Paused ⏸️)' if is_paused else ''} 🌿")
    else:
        pomodoro_message = await channel.send(f"☕ Pomodoro Timer: {time_string} {'(Paused ⏸️)' if is_paused else ''} 🌿")
        await pomodoro_message.pin()

async def pomodoro_timer(channel, duration):
    global remaining_time, pomodoro_running, is_paused, pomodoro_message
    remaining_time = duration
    pomodoro_running = True
    await update_timer_message(channel, duration)
    while remaining_time > 0 and pomodoro_running:
        if not is_paused:
            await update_timer_message(channel, remaining_time)
            await asyncio.sleep(1)
            remaining_time -= 1
        else:
            await asyncio.sleep(1)
    if pomodoro_running:
        await channel.send("✨ Pomodoro timer finished! Take a moment to relax. 🍃")

    pomodoro_running = False
    if pomodoro_message:
        await pomodoro_message.unpin()
        pomodoro_message = None
    is_paused = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="📖 /help"))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="pomodoro", description="Starts a Pomodoro timer with optional minutes.")
async def pomodoro(interaction: discord.Interaction, minutes: int = 25): # minutes parameter with default 25
    global pomodoro_running
    if pomodoro_running:
        await interaction.response.send_message("⏳ A pomodoro timer is already running. Please wait or stop the current timer. 🌿", ephemeral=True)
        return
    else:
        duration = minutes * 60
        await interaction.response.send_message(f"☕ Pomodoro timer started for {minutes} minutes! 🌿", ephemeral=True)
        asyncio.create_task(pomodoro_timer(interaction.channel, duration))

@bot.tree.command(name="stop", description="Stops the currently running timer.")
async def stop(interaction: discord.Interaction):
    global pomodoro_running
    if pomodoro_running:
        pomodoro_running = False
        await interaction.response.send_message("🛑 Pomodoro timer stopped. Take a deep breath. 🌬️")
    else:
        await interaction.response.send_message("🚫 No pomodoro timer is running. 😌", ephemeral=True)

@bot.tree.command(name="pause", description="Pauses the timer.")
async def pause(interaction: discord.Interaction):
    global is_paused, remaining_time
    is_paused = True
    await interaction.response.send_message("⏸️ Pomodoro timer paused. You deserve a moment. 🧘")
    await update_timer_message(interaction.channel, remaining_time)

@bot.tree.command(name="resume", description="Resumes the paused timer.")
async def resume(interaction: discord.Interaction):
    global is_paused, remaining_time
    is_paused = False
    await interaction.response.send_message("▶️ Pomodoro timer resumed. Back to focus! 📝")
    await update_timer_message(interaction.channel, remaining_time)

@bot.tree.command(name="skip", description="Skips to the next timer.")
async def skip(interaction: discord.Interaction):
    global pomodoro_running, remaining_time
    if pomodoro_running:
        remaining_time = 0
        await interaction.response.send_message("⏭️ Timer skipped. On to the next phase! 🌈")
        await update_timer_message(interaction.channel, remaining_time)
    else:
        await interaction.response.send_message("🚫 No pomodoro timer is running. 😌", ephemeral=True)

@bot.tree.command(name="clear", description="Clears the specified number of messages.")
async def clear(interaction: discord.Interaction, amount: int):
    if interaction.user.guild_permissions.manage_messages:
        try:
            await interaction.response.defer()
            await interaction.channel.purge(limit=amount + 1)
            await interaction.followup.send(f"🧹 Cleared {amount} messages. A fresh start! ✨")
        except discord.Forbidden:
            await interaction.response.send_message("🔒 I do not have permissions to delete messages. 😔", ephemeral=True)
    else:
        await interaction.response.send_message("🚫 You do not have permission to use this command. 🚫", ephemeral=True)

@bot.tree.command(name="help", description="Displays this help message.")
async def help_command(interaction: discord.Interaction):
    help_message = """
    📖 **Pomodoro Bot Help** 📖
    `/pomodoro [minutes]`: Starts a Pomodoro timer with optional minutes (default 25). ☕
    `/stop`: Stops the currently running timer. 🛑
    `/pause`: Pauses the timer. ⏸️
    `/resume`: Resumes the paused timer. ▶️
    `/skip`: Skips to the next timer. ⏭️
    `/clear <amount>`: Clears the specified number of messages. 🧹
    `/help`: Displays this help message. 📖
    """
    await interaction.response.send_message(help_message, ephemeral=True)

bot.run(TOKEN)