import io
import librosa
import soundfile as sf
from pathlib import Path
from aiogram import types, Bot

async def process_voice_file(file: types.File, bot: Bot) -> io.BytesIO:
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    local_file_path = temp_dir / "voice.ogg"

    await bot.download_file(file.file_path, destination=str(local_file_path))

    y, sr = librosa.load(local_file_path, sr=16000)
    wav_file = io.BytesIO()
    sf.write(wav_file, y, sr, format='WAV', subtype='PCM_16')
    wav_file.seek(0)

    local_file_path.unlink()
    return wav_file