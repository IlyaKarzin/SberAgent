import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Функция для обработки команды /start
async def start(update: Update, context):
    await update.message.reply_text(f"Привет, {update.effective_user.first_name}! Я чат-бот на основе GigaChat.")

# Функция для обработки текстовых сообщений из Telegram и ответа
async def chat_response(update: Update, context):
    user_message = update.message.text
    thread_id = str(update.effective_user.id)  # Используем user_id в качестве thread_id
    config = {"configurable": {"thread_id": thread_id}}

    # Логируем сообщение пользователя
    print("User:", user_message)

    # Получаем объект `agent` из контекста приложения
    agent = context.application.bot_data['agent']

    # Получаем ответ от GigaChat
    response = agent.invoke({"messages": [("user", user_message)]}, config=config)
    assistant_reply = response["messages"][-1].content

    # Отправляем ответ пользователю в Telegram
    await update.message.reply_text(assistant_reply)
    print("Assistant:", assistant_reply)

# Функция для инициализации Telegram-бота
def initBot(agent):
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.bot_data['agent'] = agent

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_response))

    print("Бот запущен!")
    app.run_polling()  # Бот будет работать и ждать сообщения