import sys
import os
import json

BOT_TOKEN = None
GEMINI_KEY = None
DEBUG_MODE = False
CONTENT_DATA = {}

def load_config():
    global BOT_TOKEN, GEMINI_KEY, DEBUG_MODE, CONTENT_DATA

    for arg in sys.argv:
        if arg.startswith("--token="):
            BOT_TOKEN = arg.split("=")[1]
        elif arg.startswith("--gemini="):
            GEMINI_KEY = arg.split("=")[1]
        elif arg == "--debug":
            DEBUG_MODE = True

    if not BOT_TOKEN:
        BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not GEMINI_KEY:
        GEMINI_KEY = os.getenv("GEMINI_KEY")


    content_path = "content.json"
    if os.path.exists(content_path):
        try:
            with open(content_path, "r", encoding="utf-8") as f:
                CONTENT_DATA = json.load(f)
        except Exception as e:
            print(f"Ошибка чтения контента из {content_path}: {e}")
            sys.exit(1)
    else:
        print(f"Критическая ошибка: Файл {content_path} не найден!")
        sys.exit(1)


    if not BOT_TOKEN:
        print("\n" + "=" * 60)
        print(" ОШИБКА: Telegram Bot Token не найден!")
        print("Запустите бота корректно:")
        print("python main.py --token=ТВОЙ_ТОКЕН [--gemini=КЛЮЧ_ИИ] [--debug]")
        print("=" * 60 + "\n")
        sys.exit(1)


load_config()