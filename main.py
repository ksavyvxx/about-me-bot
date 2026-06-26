import telebot
from telebot import types
import config
from validators import validate_feedback, check_secret_code

telebot.apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot(config.BOT_TOKEN)

try:
    if config.GEMINI_KEY:
        from google.genai import Client
        from google.genai import types as ai_types

        ai_client = Client(api_key=config.GEMINI_KEY)
    else:
        ai_client = None
except Exception as e:
    ai_client = None
    if config.DEBUG_MODE:
        print(f"[DEBUG AI Инициализация Ошибка]: {e}")

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton("👤 Обо мне"),
        types.KeyboardButton("🎯 Моя Цель"),
        types.KeyboardButton("🚀 Как я пришел в IT"),
        types.KeyboardButton("🧠 Мой ментор"),
        types.KeyboardButton("📈 Точка А → Точка Б"),
        types.KeyboardButton("🧩 Хобби"),
        types.KeyboardButton("💻 Мои лучшие работы"),
        types.KeyboardButton("🐙 GitHub и Ссылки")
    )
    return markup

def get_interactive_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📝 Оставить отзыв", callback_data="nav_feedback"),
        types.InlineKeyboardButton("💬 Задать вопрос ии обо мне", callback_data="nav_ai")
    )
    return markup

@bot.middleware_handler(update_types=['message'])
def log_messages(bot_instance, message):
    if config.DEBUG_MODE:
        log_text = message.text if message.text else f"[{message.content_type.upper()}]"
        username = message.from_user.username or message.from_user.id
        print(f"[DEBUG LOG] Пользователь @{username} отправил: {log_text}")


@bot.message_handler(commands=['start', 'help', 'about', 'goal', 'mentor', 'progress', 'hobbies', 'history', 'works'])
def handle_commands(message):
    try:
        if not message.text:
            return
        cmd = message.text.split()[0].lower()

        if cmd in ['/start', '/help']:
            welcome = (
                "Привет!\n\n"
                "Это мое портфолио в формате Telegram-бота.\n"
                "Здесь можно узнать информацию обо мне, моих проектах и обучении в Cap Education.\n\n"
                "Выберите нужный раздел с помощью кнопок ниже."
            )
            bot.send_message(message.chat.id, welcome, parse_mode="HTML", reply_markup=get_main_keyboard())
            bot.send_message(message.chat.id, "Дополнительные интерактивные функции:", reply_markup=get_interactive_keyboard())

        elif cmd == '/about':
            bot.send_message(message.chat.id, config.CONTENT_DATA.get("about", ""), reply_markup=get_main_keyboard())
        elif cmd == '/goal':
            bot.send_message(message.chat.id, config.CONTENT_DATA.get("goal", ""), reply_markup=get_main_keyboard())
        elif cmd == '/mentor':
            bot.send_message(message.chat.id, config.CONTENT_DATA.get("mentor", ""), reply_markup=get_main_keyboard())
        elif cmd == '/progress':
            bot.send_message(message.chat.id, config.CONTENT_DATA.get("progress", ""), reply_markup=get_main_keyboard())
        elif cmd == '/hobbies':
            bot.send_message(message.chat.id, config.CONTENT_DATA.get("hobbies", ""), reply_markup=get_main_keyboard())
        elif cmd == '/history':
            bot.send_message(message.chat.id, config.CONTENT_DATA.get("history", ""), reply_markup=get_main_keyboard())
        elif cmd == '/works':
            works = config.CONTENT_DATA.get("works", [])
            response = "🚀 <b>Мои лучшие проекты на курсе:</b>\n\n"
            for index, work in enumerate(works, 1):
                response += f"{index}. <b>{work['title']}</b>\n"
                response += f"📝 <i>Описание:</i> {work['description']}\n"
                response += f"🔗 <a href='{work['link']}'>Посмотреть на GitHub</a>\n\n"
            bot.send_message(message.chat.id, response, parse_mode="HTML", disable_web_page_preview=True)

    except Exception as e:
        if config.DEBUG_MODE:
            print(f"[ERROR] Ошибка в командах: {e}")


@bot.message_handler(content_types=['text'])
def handle_text_menu(message):
    try:
        text = message.text

        if "Обо мне" in text:
            bot.send_message(message.chat.id, config.CONTENT_DATA.get("about", ""))
        elif "Моя Цель" in text:
            bot.send_message(message.chat.id, config.CONTENT_DATA.get("goal", ""))
        elif "Как я пришел в IT" in text:
            bot.send_message(message.chat.id, config.CONTENT_DATA.get("history", ""))
        elif "Мой ментор" in text:
            bot.send_message(message.chat.id, config.CONTENT_DATA.get("mentor", ""))
        elif "Точка А" in text:
            bot.send_message(message.chat.id, config.CONTENT_DATA.get("progress", ""))
        elif "Хобби" in text:
            bot.send_message(message.chat.id, config.CONTENT_DATA.get("hobbies", ""))

        elif "Мои лучшие работы" in text:
            works = config.CONTENT_DATA.get("works", [])
            response = "🚀 <b>Мои лучшие проекты на курсе:</b>\n\n"
            for index, work in enumerate(works, 1):
                response += f"{index}. <b>{work['title']}</b>\n"
                response += f"📝 <i>Описание:</i> {work['description']}\n"
                response += f"🔗 <a href='{work['link']}'>Посмотреть на GitHub</a>\n\n"
            bot.send_message(message.chat.id, response, parse_mode="HTML", disable_web_page_preview=True)

        elif "GitHub и Ссылки" in text:
            github_url = "https://github.com/ksavyvxx/about-me-bot"
            bot.send_message(message.chat.id, f"📂 <b>Исходный код этого бота:</b>\n{github_url}\n\n", disable_web_page_preview=True)

        else:
            if check_secret_code(text):
                bot.send_message(message.chat.id, "🎉 <b>Ого! Вы нашли секретную пасхалку!</b> 🎉\nСпасибо за внимательную проверку кода", parse_mode="HTML")
                sticker_id1 = 'CAACAgIAAxkBAAERcrtqPYATL0kRwvpjpAABYFlXhG1fud0AAhChAAIJRihIQLZ73BaqLlE8BA'
                bot.send_sticker(message.chat.id, sticker_id1)
            else:
                bot.send_message(message.chat.id, "Пожалуйста, выберите раздел на клавиатуре или воспользуйтесь кнопками под приветственным сообщением.")

    except Exception as e:
        bot.send_message(message.chat.id, "Произошла непредвиденная ошибка в обработке меню. Но бот продолжает работу!")
        if config.DEBUG_MODE:
            print(f"[ERROR] Ошибка текстового меню: {e}")



@bot.callback_query_handler(func=lambda call: call.data.startswith('nav_'))
def handle_callbacks(call):
    try:
        bot.answer_callback_query(call.id)

        if call.data == "nav_feedback":
            msg = bot.send_message(
                call.message.chat.id,
                "📝Ваш отзыв📝\n\n"
                "Отправьте сообщение в формате <code>ваш_email: текст_отзыва</code>.\n"
                "Пример: <code>cap_edu@gmail.com: Отличная архитектура проекта продолжай в том же духе!</code>",
                parse_mode="HTML"
            )
            bot.register_next_step_handler(msg, process_feedback_step)

        elif call.data == "nav_ai":
            if not ai_client:
                bot.send_message(call.message.chat.id, "Извините, ии-модуль не был запущен, так как при старте скрипта не передан или не определен ключ 'gemini'.")
                return

            msg = bot.send_message(call.message.chat.id, "<b>🤖Спросите ии обо мне🤖</b>\nЗадайте любой вопрос в свободной форме:", parse_mode="HTML")
            bot.register_next_step_handler(msg, process_ai_step)

    except Exception as e:
        if config.DEBUG_MODE:
            print(f"[ERROR] Ошибка в callback: {e}")



def process_feedback_step(message):
    try:
        if not message.text:
            bot.send_message(message.chat.id, "Неверный ввод. Требуется текстовое сообщение.")
            return


        if message.text.startswith('/') or any(k in message.text for k in ["Обо мне", "Цель", "Ментор", "Работы", "Ссылки"]):
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            handle_text_menu(message)
            return

        parsed = validate_feedback(message.text)
        if parsed:
            success_text = (
                f"<b>Email:</b> <code>{parsed['email']}</code>\n"
                f"<b>Отзыв:</b> {parsed['text']}\n"
                "Спасибо за фидбек! Данные успешно обработаны."
            )
            bot.send_message(message.chat.id, success_text, parse_mode="HTML")
            sticker_id = 'CAACAgIAAxkBAAERI0Bp8gdCrIa4BawvZuvcCwzKnKQtygACPkIAApgVUUmzPMRn8E6HNDsE'
            bot.send_sticker(message.chat.id, sticker_id)
        else:
            bot.send_message(message.chat.id, "Формат сообщения не соответствует шаблону `email:текст`. Попробуйте еще раз через интерактивное меню.")
    except Exception as e:
        if config.DEBUG_MODE:
            print(f"[ERROR] Ошибка в шаге валидации: {e}")


def process_ai_step(message):
    try:
        if not message.text:
            bot.send_message(message.chat.id, " Пожалуйста, напишите текстовый вопрос.")
            return


        if message.text.startswith('/') or any(k in message.text for k in ["Обо мне", "Цель", "ментор", "работы", "Ссылки"]):
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            handle_text_menu(message)
            return

        bot.send_chat_action(message.chat.id, 'typing')

        about_context = config.CONTENT_DATA.get("about", "")
        mentor_context = config.CONTENT_DATA.get("mentor", "")

        system_instruction_text = (
            f"Вот информация об авторе бота (твоем студенте): {about_context}. "
            f"Вот информация о его обучении и менторе: {mentor_context}. "
            "Твой ответ должен быть емким и структурированным, укладываться в рамки 3-4 абзацев"
        )

        contents = [
            ai_types.Content(
                role="user",
                parts=[ai_types.Part.from_text(text=message.text)],
            ),
        ]

        generate_content_config = ai_types.GenerateContentConfig(
            system_instruction=[ai_types.Part.from_text(text=system_instruction_text)],
        )

        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=generate_content_config,
        )

        if response and response.text:
            ai_text = response.text
            if len(ai_text) > 4000:
                ai_text = ai_text[:3900] + "...\n\n[Текст ответа был автоматически сокращен]"

            bot.send_message(message.chat.id, f"Ответ ИИ:\n\n{ai_text}")
        else:
            bot.send_message(message.chat.id, "ИИ не смог сгенерировать ответ. Попробуйте перефразировать вопрос.")

    except Exception as e:
        bot.send_message(message.chat.id, "Ой, нейросеть ненадолго задумалась. Попробуйте отправить запрос еще раз через минуту.")
        if config.DEBUG_MODE:
            print(f"[ERROR] {type(e).__name__}: {e}")

if __name__ == "__main__":
    print("бот запущен успешно!")
    if config.DEBUG_MODE:
        print("Активен режим DEBUG логов в консоли.")

    bot.infinity_polling()