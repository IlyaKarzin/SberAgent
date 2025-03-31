from GigaChat.chat import initChat
from Telegram.bot import initBot

if __name__ == "__main__":
    agent = initChat()
    initBot(agent)