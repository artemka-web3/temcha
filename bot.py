import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

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
user_data = {}

# Инициализация бота
TOKEN = "7566625979:AAHvtbpKS2KA7aJWydiVAzyyfrFC1K4AGnQ"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Давай начнем тест по истории России. Нажми /quiz, чтобы начать!")

@dp.message_handler(commands=['quiz'])
async def quiz(message: types.Message):
    chat_id = message.chat.id
    user_data[chat_id] = {"score": 0, "question_index": 0}
    await ask_question(chat_id)

async def ask_question(chat_id):
    user = user_data.get(chat_id)

    if not user:
        await bot.send_message(chat_id, "Начните тест с команды /quiz.")
        return

    question_index = user["question_index"]

    if question_index < len(questions):
        question = questions[question_index]
        options = question["options"]

        keyboard = InlineKeyboardMarkup()
        for i, option in enumerate(options):
            keyboard.add(InlineKeyboardButton(option, callback_data=str(i)))

        await bot.send_message(chat_id, question["question"], reply_markup=keyboard)
    else:
        score = user["score"]
        await bot.send_message(chat_id, f"Тест завершен! Ты ответил правильно на {score} из {len(questions)} вопросов.")
        del user_data[chat_id]

@dp.callback_query_handler()
async def button(query: CallbackQuery):
    chat_id = query.message.chat.id

    if chat_id not in user_data:
        await query.answer()
        await query.message.edit_text("Начните тест с команды /quiz.")
        return

    user = user_data[chat_id]
    question_index = user["question_index"]
    selected_option = int(query.data)

    # Проверяем ответ
    if selected_option == questions[question_index]["answer"]:
        user["score"] += 1

    user["question_index"] += 1

    await query.answer()
    if user["question_index"] < len(questions):
        await next_question(chat_id)
    else:
        await query.message.edit_text(
            f"Тест завершен! Ты ответил правильно на {user['score']} из {len(questions)} вопросов."
        )
        del user_data[chat_id]

async def next_question(chat_id):
    user = user_data[chat_id]

    question_index = user["question_index"]
    question = questions[question_index]
    options = question["options"]

    keyboard = InlineKeyboardMarkup()
    for i, option in enumerate(options):
        keyboard.add(InlineKeyboardButton(option, callback_data=str(i)))

    await bot.send_message(chat_id, question["question"], reply_markup=keyboard)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
