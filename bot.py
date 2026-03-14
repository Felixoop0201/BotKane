import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ ОШИБКА: Укажи BOT_TOKEN в файле .env!")
    exit()

# --- АДМИН ---
ADMIN_USERNAME = "nukakbaladno"  # без @

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ПРОВЕРКА АДМИНА ---
def is_admin(user: types.User) -> bool:
    return user.username == ADMIN_USERNAME

# --- КЛАВИАТУРЫ ---

def main_menu_kb():
    keyboard = [
        [InlineKeyboardButton(text="👤 Обо мне", callback_data="about_me")],
        [InlineKeyboardButton(text="🚀 Мои проекты", callback_data="projects")],
        [InlineKeyboardButton(text="🛠 Навыки", callback_data="skills")],
        [InlineKeyboardButton(text="📩 Заказать проект", url="https://t.me/nukakbaladno")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def back_kb():
    keyboard = [[InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def projects_kb():
    keyboard = [
        [InlineKeyboardButton(text="📊 CS2 Vizer", callback_data="proj_cs2")],
        [InlineKeyboardButton(text="🤖 Бот-портфолио", callback_data="proj_portfolio_bot")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def admin_kb():
    keyboard = [
        [InlineKeyboardButton(text="✏️ Инфо обо мне", callback_data="admin_edit_about")],
        [InlineKeyboardButton(text="➕ Добавить проект", callback_data="admin_add_project")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# --- СЧЁТЧИК ПОЛЬЗОВАТЕЛЕЙ (простой, в памяти) ---
unique_users = set()

# --- ХЭНДЛЕРЫ ---

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    unique_users.add(message.from_user.id)

    greeting = (
        f"Привет, {message.from_user.first_name} 👋\n\n"
        "Я <b>Felix Kane</b> — разрабатываю Telegram-ботов, "
        "веб-сервисы и интегрирую AI в проекты.\n\n"
        "Здесь можешь посмотреть мои работы и связаться для заказа."
    )

    # Если это админ — показываем особое приветствие
    if is_admin(message.from_user):
        greeting += "\n\n<i>👑 Ты вошёл как администратор. /admin для управления.</i>"

    await message.answer(greeting, parse_mode="HTML", reply_markup=main_menu_kb())


@dp.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if not is_admin(message.from_user):
        await message.answer("⛔️ У тебя нет доступа к этой команде.")
        return

    await message.answer(
        "👑 <b>Панель администратора</b>\n\nЧто хочешь сделать?",
        parse_mode="HTML",
        reply_markup=admin_kb()
    )


@dp.callback_query()
async def callbacks_handler(callback: types.CallbackQuery):
    action = callback.data
    user = callback.from_user

    # --- Обо мне ---
    if action == "about_me":
        text = (
            "👤 <b>Felix Kane</b>\n\n"
            "Разрабатываю Telegram-ботов, веб-сервисы и AI-инструменты на Python.\n\n"
            "Работаю с современными языковыми моделями — Claude, Gemini, OpenRouter. "
            "Умею встроить AI в реальный проект под конкретную задачу, "
            "а не просто подключить ChatGPT.\n\n"
            "Есть запущенные проекты в портфолио. "
            "Берусь за задачи разной сложности, работаю честно — "
            "если задача не по силам, скажу сразу."
        )
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_kb())

    # --- Навыки ---
    elif action == "skills":
        text = (
            "🛠 <b>Навыки:</b>\n\n"
            "• Python — основной язык\n"
            "• Telegram Bot API / aiogram 3\n"
            "• AI интеграции (Claude, Gemini, OpenRouter)\n"
            "• Веб-сервисы, REST API\n"
            "• Базы данных (SQLite, PostgreSQL)\n"
            "• Деплой на Render / Railway\n"
            "• HTML, CSS, JavaScript (базовый фронтенд)"
        )
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_kb())

    # --- Проекты ---
    elif action == "projects":
        await callback.message.edit_text(
            "🚀 <b>Мои проекты:</b>\n\nВыбери проект чтобы узнать подробнее:",
            parse_mode="HTML",
            reply_markup=projects_kb()
        )

    # --- CS2 Vizer ---
    elif action == "proj_cs2":
        text = (
            "📊 <b>CS2 Vizer</b>\n\n"
            "Веб-сервис для трейдеров скинами CS2.\n\n"
            "• Загрузка инвентаря Steam\n"
            "• Калькулятор прибыли со сделок\n"
            "• Сохранение истории сделок\n"
            "• AI-агент который анализирует каждую сделку\n\n"
            "Задеплоен и работает в продакшене.\n"
            "🔗 cs2-calculytor.onrender.com"
        )
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_kb())

    # --- Бот-портфолио ---
    elif action == "proj_portfolio_bot":
        text = (
            "🤖 <b>Бот-портфолио</b>\n\n"
            "Интерактивное портфолио разработчика в Telegram.\n\n"
            "• Навигация через inline-кнопки\n"
            "• Разделы: обо мне, проекты, навыки\n"
            "• Панель администратора\n"
            "• Python + aiogram 3\n\n"
            "Именно этот бот — можешь оценить сам 😄"
        )
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_kb())

    # --- Админ панель ---
    elif action == "admin_stats":
        if not is_admin(user):
            await callback.answer("⛔️ Нет доступа", show_alert=True)
            return
        text = (
            f"📊 <b>Статистика</b>\n\n"
            f"👥 Уникальных пользователей: {len(unique_users)}"
        )
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=admin_kb())

    elif action in ("admin_edit_about", "admin_add_project"):
        if not is_admin(user):
            await callback.answer("⛔️ Нет доступа", show_alert=True)
            return
        await callback.answer("🔧 Функция в разработке", show_alert=True)

    # --- Назад ---
    elif action == "back_to_main":
        text = (
            "Я <b>Felix Kane</b> — разрабатываю Telegram-ботов, "
            "веб-сервисы и интегрирую AI в проекты.\n\n"
            "Здесь можешь посмотреть мои работы и связаться для заказа."
        )
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=main_menu_kb())

    await callback.answer()


async def main():
    print("🚀 Бот-портфолио Felix Kane запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
