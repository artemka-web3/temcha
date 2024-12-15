import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import json

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Вопросы и ответы
questions = [
    {        "question": "Какое событие считается началом Древнерусского государства?",
        "options": ["Куликовская битва", "Призвание варягов", "Крещение Руси", "Установление монгольского ига"],        "answer": 1
    },    {
        "question": "Кто был первым князем Киевской Руси?",        "options": ["Владимир Святославич", "Олег Вещий", "Ярослав Мудрый", "Игорь Рюрикович"],
        "answer": 1    },
    {        "question": "Когда произошло крещение Руси?",
        "options": ["988 год", "862 год", "1240 год", "1237 год"],        "answer": 0
    },    {
        "question": "Какое событие произошло в 1242 году?",        "options": ["Битва на Калке", "Невская битва", "Ледовое побоище", "Куликовская битва"],
        "answer": 2    },
    {        "question": "Кто был основателем Московского княжества?",
        "options": ["Иван III", "Юрий Долгорукий", "Дмитрий Донской", "Василий II"],        "answer": 1
    },    {
        "question": "Когда была основана Москва?",        "options": ["1147 год", "1237 год", "1380 год", "1480 год"],
        "answer": 0    },
    {        "question": "Кто был первым царем России?",
        "options": ["Иван IV (Грозный)", "Петр I", "Алексей Михайлович", "Федор I"],        "answer": 0
    },    {
        "question": "Какое событие произошло в 1612 году?",        "options": ["Опричнина", "Освобождение Москвы от польских интервентов", "Смута", "Установление династии Романовых"],
        "answer": 1    },
    {        "question": "Кто из царей провел реформы, известные как 'Петровские реформы'?",
        "options": ["Николай II", "Петр I", "Екатерина II", "Иван III"],        "answer": 1
    },    {
        "question": "Когда была проведена первая общероссийская перепись населения?",        "options": ["1719 год", "1722 год", "1763 год", "1795 год"],
        "answer": 0    },
    {        "question": "Какой документ был принят в 1861 году, отменяющий крепостное право?",
        "options": ["Устав о губерниях", "Манифест об освобождении крестьян", "Устав о земстве", "Конституция"],        "answer": 1
    },    {
        "question": "Кто был последним императором России?",        "options": ["Николай I", "Александр III", "Николай II", "Петр II"],
        "answer": 2    },
    {        "question": "Когда произошла Февральская революция?",
        "options": ["1905 год", "1917 год", "1922 год", "1914 год"],        "answer": 1
    },    {
        "question": "Какое событие произошло в октябре 1917 года?",        "options": ["Октябрьская революция", "Битва под Москвой", "Подписание Брестского мира", "Гражданская война"],
        "answer": 0    },
    {        "question": "Когда была принята новая Конституция Российской Федерации?",
        "options": ["1991 год", "1993 год", "1995 год", "2000 год"],        "answer": 1
    }]

# Хранение состояния пользователей
USER_DATA_FILE = "user_data.json"

# Инициализация бота
TOKEN = "7566625979:AAHvtbpKS2KA7aJWydiVAzyyfrFC1K4AGnQ"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

def load_user_data():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Функция для сохранения данных пользователей
def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file)

# Инициализация данных пользователей
user_data = load_user_data()

# Команда /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Давай начнем тест по истории России. Нажми /quiz, чтобы начать!")

# Команда /quiz
@dp.message_handler(commands=['quiz'])
async def quiz(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in user_data:
        user_data[user_id] = {"score": 0, "question_index": 0}
    else:
        user_data[user_id]["score"] = 0
        user_data[user_id]["question_index"] = 0
    save_user_data(user_data)
    await ask_question(message.chat.id, user_id)

# Функция для отправки вопроса
async def ask_question(chat_id, user_id):
    user = user_data[user_id]
    question_index = user["question_index"]

    if question_index < len(questions):
        question = questions[question_index]
        options = question["options"]

        keyboard = InlineKeyboardMarkup()
        for i, option in enumerate(options):
            keyboard.add(InlineKeyboardButton(option, callback_data=f"{user_id}:{i}"))

        await bot.send_message(chat_id, question["question"], reply_markup=keyboard)
    else:
        score = user["score"]
        await bot.send_message(chat_id, f"Тест завершен! Ты ответил правильно на {score} из {len(questions)} вопросов.")
        user_data[user_id]["question_index"] = 0
        user_data[user_id]["score"] = 0
        save_user_data(user_data)

# Обработчик ответов
@dp.callback_query_handler(lambda callback_query: True)
async def handle_answer(callback_query: types.CallbackQuery):
    user_id, selected_option = callback_query.data.split(":")
    selected_option = int(selected_option)

    if user_id not in user_data:
        await callback_query.answer("Начните тест с команды /quiz.", show_alert=True)
        return

    user = user_data[user_id]
    question_index = user["question_index"]

    # Проверяем ответ
    if selected_option == questions[question_index]["answer"]:
        user["score"] += 1

    user["question_index"] += 1
    save_user_data(user_data)

    await callback_query.answer()

    if user["question_index"] < len(questions):
        await ask_question(callback_query.message.chat.id, user_id)
    else:
        await bot.send_message(
            callback_query.message.chat.id,
            f"Тест завершен! Ты ответил правильно на {user['score']} из {len(questions)} вопросов."
        )
        user_data[user_id]["question_index"] = 0
        user_data[user_id]["score"] = 0
        save_user_data(user_data)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)