from pyrogram import Client, filters  
from pytgcalls import PyTgCalls, StreamType  
from pytgcalls.types.input_stream import AudioPiped  
import yt_dlp  

API_ID = "22654424"  
API_HASH = "17ec8842a924d03e88a0c458064deeb"  
BOT_TOKEN = "7550486569:AAFPbUeAHis3Z3929OcF1MPV7lcLtmK8Tt4"  

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)  
call = PyTgCalls(app)  

def get_audio(url):  
    options = {"format": "bestaudio/best"}  
    with yt_dlp.YoutubeDL(options) as ydl:  
        info = ydl.extract_info(url, download=False)  
        return info["url"]  

@app.on_message(filters.command("play"))  
async def play_music(client, message):  
    chat_id = message.chat.id  
    if len(message.command) < 2:  
        await message.reply("Please provide a YouTube link.")  
        return  
      
    url = message.command[1]  
    audio_url = get_audio(url)  
    await call.join_group_call(chat_id, AudioPiped(audio_url, StreamType().pulse_stream))  
    await message.reply(f"Now playing: {url}")  

@app.on_message(filters.command("stop"))  
async def stop_music(client, message):  
    chat_id = message.chat.id  
    await call.leave_group_call(chat_id)  
    await message.reply("Stopped the music.")  

app.start()  
call.start()  
print("Bot is running...")  
app.idle()
