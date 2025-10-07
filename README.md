# Woody
# 🎵 Discord Music Bot

A simple Discord bot built with **discord.py** and **yt-dlp** that can join voice channels, play music from YouTube, manage a queue, and disconnect automatically after inactivity.  

---

## ✨ Features

- 🔊 **Join / Leave voice channels** (`!join`, `!leave`)  
- 🎶 **Play music** with YouTube search (`!p <query>`)  
- ➕ **Queue system** to add multiple tracks (`!queue`)  
- ⏭️ **Skip songs** (`!skip`)  
- ⏹️ **Stop and disconnect** (`!stop`)  
- 🏓 **Ping command** to check latency (`!ping`)  
- ⏱️ **Uptime tracking** (`!uptime`)  
- ⏲️ **Auto-disconnect after inactivity** (default: 15 min, configurable with `!settimeout <minutes>`)  

---

## ⚙️ How It Works

1. **Join a voice channel** with `!join`  
2. **Play a track** using `!p <song name or YouTube link>`  
   - The bot searches YouTube with `yt-dlp` and streams audio with FFmpeg  
3. **Queue multiple songs** – they will play in order  
4. **Skip** with `!skip` or **stop** with `!stop`  
5. If idle for too long, the bot **auto-disconnects**  

---

## 📦 Dependencies

- [discord.py](https://github.com/Rapptz/discord.py)  
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)  
- FFmpeg installed and available in your system PATH  

Install with:

```bash
pip install -U discord.py yt-dlp

