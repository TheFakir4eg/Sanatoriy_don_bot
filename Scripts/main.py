import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import CommandStart
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Пути к файлам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Определяем корневую папку проекта
FILES_DIR = os.path.join(BASE_DIR, "Files")  # Путь к папке files

spa_services_PDF_FILE_PATH = os.path.join(FILES_DIR, "spa_services.pdf")  # PDF-файл
THUMBNAIL_PATH = os.path.join(FILES_DIR, "spa_services_preview.jpg")  # Миниатюра

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция отправки PDF-файла с предпросмотром
async def send_pdf_spa_services(callback: types.CallbackQuery):
    try:
        pdf_file = FSInputFile(spa_services_PDF_FILE_PATH)
        thumb_file = FSInputFile(THUMBNAIL_PATH) if os.path.exists(THUMBNAIL_PATH) else None

        await bot.send_document(
            chat_id=callback.message.chat.id,
            document=pdf_file,
            caption="Меню СПА",
            thumbnail=thumb_file
        )
        await callback.answer("Файл отправлен!")
    except FileNotFoundError:
        await callback.answer("Ошибка: файл не найден.")
    except Exception as e:
        logging.error(f"Ошибка при отправке PDF: {e}", exc_info=True)
        await callback.answer("Произошла ошибка при отправке файла.")


# Функция для создания главного меню
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Проживание", callback_data="living")],
        [InlineKeyboardButton(text="Ресторан", callback_data="restoran")],
        [InlineKeyboardButton(text="СПА", callback_data="spa")],
        [InlineKeyboardButton(text="Медицина", callback_data="medicine")],
        [InlineKeyboardButton(text="Программа лояльности ЛОГУС", callback_data="loyalty")]
    ])
    return keyboard

# Функция для создания меню Проживание
def get_submenu_living():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Технические проблемы", callback_data='tech_problem')],
        [InlineKeyboardButton(text="Подключение к Wi-Fi", callback_data="WiFi_connecting")],
        [InlineKeyboardButton(text="Запрос дополнительных принадлежностей", callback_data="dop_asking")],
        [InlineKeyboardButton(text="График работы шведской линии", callback_data="unlimit_food_graf")],
        [InlineKeyboardButton(text="Связаться с менеджером", callback_data="connecting_to_manager")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])
    return keyboard

# Функция для создания меню Проживание - Технические проблемы
def get_submenu_tech_problem():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Проблемы с электричеством", callback_data='electric_problem')],
        [InlineKeyboardButton(text="Проблемы с водоснабжением", callback_data='water_problem')],
        [InlineKeyboardButton(text="Некомфортная температура в номере", callback_data='temp_problem')],
        [InlineKeyboardButton(text="Проблемы с сейфом", callback_data='safe_problem')],
        [InlineKeyboardButton(text="Неисправен ТВ", callback_data='tv_problem')],
        [InlineKeyboardButton(text="Другой вопрос", callback_data='another_problem')],
        [InlineKeyboardButton(text="Назад", callback_data="living_back")]
    ])
    return keyboard

# Функция для создания подменю Ресторан
def get_submenu_restoran():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Время работы кофейни и ресторана", callback_data='restoran_work_time')],
        [InlineKeyboardButton(text="Меню ресторана\рум-сервиса", callback_data='restoran_eat_menu')],
        [InlineKeyboardButton(text="Оформить заказ в номер", callback_data='restoran_order')],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])
    return keyboard

# Функция для создания подменю 2
def get_submenu_spa():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Бронирование услуг", callback_data='spa_bron')],
        [InlineKeyboardButton(text="Меню", callback_data='spa_menu_check')],
        [InlineKeyboardButton(text="Связь с менеджером", callback_data='spa_call_manager')],
        [InlineKeyboardButton(text="Акции", callback_data='spa_skidki')],
        [InlineKeyboardButton(text="Как добраться?", callback_data='spa_route')],
        [InlineKeyboardButton(text="Оставить отзыв", callback_data='spa_call_back')],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])
    return keyboard

# Функция для создания подменю 2
def get_submenu_medicine():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="В разработке", callback_data="medicine_1")],
        #[InlineKeyboardButton(text="Опция 2.2", callback_data="sub2_2")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])
    return keyboard

# Функция для создания подменю 1
def get_submenu_loyalty():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Зарегистрироваться", url="https://loyalty.donresort.ru/")],
        [InlineKeyboardButton(text="Привилегии участников программы", callback_data='loyality_privileges')],
        [InlineKeyboardButton(text="📄 Правила участия в программе лояльности", callback_data='loyality_rules')],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])
    return keyboard

# Обработчик команды /start
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Добро пожаловать в Санаторий Дон! \nВыберите интересующую вас категорию в меню ниже", reply_markup=get_main_keyboard())

# Обработчик нажатий инлайн-кнопок
@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    # обработка основного меню
    if callback.data == "living":
        await callback.message.edit_text("Выберите опцию:", reply_markup=get_submenu_living())
    elif callback.data == "restoran":
        await callback.message.edit_text("Выберите опцию:", reply_markup=get_submenu_restoran())
    elif callback.data == "spa":
        await callback.message.edit_text("Выберите опцию:", reply_markup=get_submenu_spa())   
    elif callback.data == "medicine":
        await callback.message.edit_text("Выберите опцию:", reply_markup=get_submenu_medicine())   
    elif callback.data == "loyalty":
        await callback.message.edit_text("Выберите опцию:", reply_markup=get_submenu_loyalty()) 
    # обработка меню Проживание    
    elif callback.data == "tech_problem":
        await callback.message.edit_text("Выберите опцию:", reply_markup=get_submenu_tech_problem())  
    elif callback.data == "spa_menu_check":
        await send_pdf_spa_services(callback)         
    elif callback.data == "sub1_1":
        await callback.message.answer("Вы выбрали Опция 1.1")
    elif callback.data == "sub1_2":
        await callback.message.answer("Вы выбрали Опция 1.2")
    elif callback.data == "sub2_1":
        await callback.message.answer("Вы выбрали Опция 2.1")
    elif callback.data == "sub2_2":
        await callback.message.answer("Вы выбрали Опция 2.2")
    elif callback.data == "living_back":
        await callback.message.edit_text("Выберите опцию:", reply_markup=get_submenu_living())     
    elif callback.data == "back":
        await callback.message.edit_text("Добро пожаловать в Санаторий Дон! \nВыберите интересующую вас категорию в меню ниже", reply_markup=get_main_keyboard())
    await callback.answer()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
