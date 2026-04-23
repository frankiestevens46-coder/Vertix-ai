import discord
import aiohttp
import urllib.parse
import random

# Config
DISCORD_TOKEN = 'MTQ5MTQyMTYzNDI2MTY4MDIwMg.GqCE-N.HARY0_M9rGZ6AMnz4EHplaOs0ac3_uVeJ-gqh4'
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# This function is now optimized for SPEED
async def get_fast_reply(prompt, style):
    # Using 'searchgpt' or 'openai' model for faster responses
    url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}?system={urllib.parse.quote(style)}&model=openai"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=15) as response:
                if response.status == 200:
                    return await response.text()
    except: return None
    return None

@client.event
async def on_ready():
    print(f'⚡ Vertix Speed-Bot is Live!')

@client.event
async def on_message(message):
    if message.author == client.user: return
    content = message.content.strip()
    low_content = content.lower()

    # --- 1. INSTANT ROAST / COMPLIMENT ---
    if low_content.startswith("!roast") or low_content.startswith("!compliment"):
        is_roast = "roast" in low_content
        target = content.split(" ", 1)[1] if " " in content else "this person"
        
        # Immediate "Typing" feel
        status = await message.reply("🔥 **Roasting...**" if is_roast else "✨ **Kindness incoming...**")
        
        style = "You are a savage comedian. Give a very short, funny 1-sentence roast." if is_roast else "Give a very short, sweet 1-sentence compliment."
        reply = await get_fast_reply(f"Write a {low_content} for {target}", style)
        await status.edit(content=reply if reply else "I'm speechless!")
        return

    # --- 2. HIGH-STAKES ADVENTURE (Faster & Better) ---
    if low_content.startswith("!adventure") or low_content.startswith("!go"):
        status = await message.reply("⚔️ **Starting Quest...**")
        
        # This tells the AI: NO MORE WAITING. Start the story NOW.
        style = (
            "You are a professional Dungeon Master. "
            "If the user says '!adventure', immediately describe a dangerous opening scene (e.g. trapped in a dungeon, facing a dragon). "
            "If they say '!go', describe the dramatic result of their action. "
            "Rules: Be vivid, keep it to 3 sentences, and always end with 'What do you do?'"
        )
        
        try:
            # We use a 30-second timeout here because stories take longer to write
            async with aiohttp.ClientSession() as session:
                url = f"https://text.pollinations.ai/{urllib.parse.quote(content)}?system={urllib.parse.quote(style)}&model=searchgpt"
                async with session.get(url, timeout=30) as response:
                    if response.status == 200:
                        reply = await response.text()
                        await status.edit(content=f"🏰 **VERTIX QUEST:**\n{reply}")
                    else:
                        await status.edit(content="❌ The Dungeon Master is busy. Try again!")
        except:
            await status.edit(content="⏳ Connection timed out. The story was too long! Try again.")
        return



    # --- 3. VIBE CHECK ---
    if low_content == "!vibe":
        status = await message.reply("🔮 **Scanning...**")
        messages = [m.content async for m in message.channel.history(limit=5)]
        style = "Analyze the mood of this chat in 5 words and 3 emojis."
        reply = await get_fast_reply(str(messages), style)
        await status.edit(content=f"**Vibe:** {reply}")
        return

    # --- 4. IMAGE (Direct Link = Instant) ---
    if low_content.startswith("!image"):
        prompt = content[7:].strip()
        status = await message.reply(f"🎨 **Drawing '{prompt}'...**")
        img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?seed={random.randint(1,999)}&nologo=true"
        await status.edit(content=img_url)
        return

    # --- 5. CHAT ---
    if low_content.startswith("!ai") or isinstance(message.channel, discord.DMChannel) or client.user.mentioned_in(message):
        status = await message.reply("💬 **Thinking...**")
        style = "You are Vertix AI. Be chill, helpful, and very brief."
        reply = await get_fast_reply(content, style)
        await status.edit(content=reply[:1990] if reply else "Server busy!")

client.run(DISCORD_TOKEN)

