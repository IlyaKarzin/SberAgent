import os
from .tools import get_all_barcode, get_barcode_data, add_barcode
from langchain_gigachat.chat_models import GigaChat
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

load_dotenv()
CHAT_TOKEN = os.getenv("CHAT_TOKEN")

def initChat():
    tools = [add_barcode, get_barcode_data, get_all_barcode]

    system_prompt = ("Ты бот-отслеживатель статуса посылок. Твоя задача добавлять номера отслеживания(не спрашивай дополнительные данные у пользователя, просто вызови функцию add_barcode), "
                     "которые попросит пользователь, "
                     "а также выдавать информацию по ноомеру послыки, который укажет пользователь")
    model = GigaChat(
        credentials=CHAT_TOKEN,
        scope="GIGACHAT_API_PERS",
        model="GigaChat",
        verify_ssl_certs=False,
    )
    agent = create_react_agent(model,
                               tools=tools,
                               checkpointer=MemorySaver(),
                               state_modifier=system_prompt)

    return agent
