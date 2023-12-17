from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import discord
from discord.ext import commands

# Discord Bot setup
bot = commands.Bot(command_prefix="!")  # You can adjust the prefix as needed

# FastAPI setup
app = FastAPI()

class CommandRequest(BaseModel):
    command: str

@app.post('/discord/command/')
async def handle_discord_command(request: CommandRequest):
    # Process the received data from Discord commands
    command = request.command
    # Process the command and perform actions as needed with the Discord bot

    return {"message": f"Received command: {command}"}

# Run FastAPI app and Discord bot
if __name__ == "__main__":
    import uvicorn
    bot.run('YOUR_DISCORD_BOT_TOKEN')  # Replace with your Discord bot token
    uvicorn.run(app, host="0.0.0.0", port=8000)