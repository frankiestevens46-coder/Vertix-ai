import discord

TOKEN = 'MTQ5MTQyMTYzNDI2MTY4MDIwMg.GqCE-N.HARY0_M9rGZ6AMnz4EHplaOs0ac3_uVeJ-gqh4' # Use your reset token here

client = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f"Syncing/Clearing commands for {client.user}...")
    # This clears ALL global slash commands
    tree.clear_commands(guild=None)
    await tree.sync()
    print("✅ All slash commands deleted from Discord's memory!")
    await client.close()

client.run(TOKEN)

