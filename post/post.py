import os
from pochta import tracking
from dotenv import load_dotenv
from database import database

load_dotenv()
POST_LOGIN = os.getenv("POST_LOGIN")
POST_PASSWORD = os.getenv("POST_PASSWORD")

# Инициализация базы данных
conn, cursor = database.init_db()
barcode_database = database.get_all_barcodes(cursor)


#barcode_database = []
def init_post():
    post_service = tracking.SingleTracker(POST_LOGIN, POST_PASSWORD)
    return post_service