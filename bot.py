import logging 
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
# Включаем логированиеlogging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
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
# Хранение состояния бота
user_data = {}
def start(update: Update, context: CallbackContext) -> None:    
    update.message.reply_text('Привет! Давай начнем тест по истории России. Нажми /quiz, чтобы начать!')

def quiz(update: Update, context: CallbackContext) -> None:
    user_data[update.message.chat_id] = {        
        "score": 0,
        "question_index": 0    
    }
    ask_question(update, context)
    
def ask_question(update: Update, context: CallbackContext) -> None:    
    user_id = update.message.chat_id
    question_index = user_data[user_id]["question_index"]    
    if question_index < len(questions):        
        question = questions[question_index]
        options = question["options"]        
        keyboard = [[InlineKeyboardButton(option, callback_data=str(i)) for i, option in enumerate(options)]]
            
            
        reply_markup = InlineKeyboardMarkup(keyboard)        
        update.message.reply_text(question["question"], reply_markup=reply_markup)
    else:        
        update.message.reply_text(f'Тест завершен! Ты ответил правильно на {user_data[user_id]["score"]} из {len(questions)} вопросов.')
        del user_data[user_id]  # Удаляем данные пользователя после завершения теста

def button(update: Update, context: CallbackContext) -> None:    
    user_id = update.callback_query.message.chat_id
    question_index = user_data[user_id]["question_index"]    
    # Проверяем правильность ответа    
    selected_option = int(update.callback_query.data)
    if selected_option == questions[question_index]["answer"]:        
        user_data[user_id]["score"] += 1
        user_data[user_id]["question_index"] += 1
    ask_question(update.callback_query, context)

def main() -> None:    # Вставьте сюда ваш токен
    TOKEN = '7566625979:AAHvtbpKS2KA7aJWydiVAzyyfrFC1K4AGnQ'    
    updater = Updater(TOKEN)
    # Получаем диспетчер для регистрации обработчиков    
    dispatcher = updater.dispatcher
    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))    
    dispatcher.add_handler(CommandHandler("quiz", quiz))
    dispatcher.add_handler(CallbackQueryHandler(button))
    # Запускаем бота    updater.start_polling()
    # Ожидаем завершения работы
    updater.idle()

if __name__ == '__main__':    
    main()