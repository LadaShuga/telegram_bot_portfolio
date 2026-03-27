import asyncio
import logging
import os
from pathlib import Path
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# Получаем абсолютный путь к папке со скриптом
BASE_DIR = Path(__file__).parent

# Берем переменные из окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = os.getenv("ADMIN_IDS", "")

# Проверяем наличие токена
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения!")

# Преобразуем ADMIN_IDS в список чисел
ADMIN_LIST = [int(id.strip()) for id in ADMIN_IDS.split(",") if id.strip()] if ADMIN_IDS else []

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Импортируем портфолио и категории
from portfolio import PORTFOLIO, BOT_PROJECTS, DESIGN_PROJECTS

# Создание бота и хранилища для FSM
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)

# ----- КЛАВИАТУРЫ -----

def start_keyboard():
    """Клавиатура с кнопкой 'Начать' (Reply-клавиатура)"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Начать")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def remove_keyboard():
    """Убирает клавиатуру"""
    return ReplyKeyboardMarkup(
        keyboard=[[]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def main_inline_keyboard():
    """Главное инлайн-меню"""
    buttons = [
        [InlineKeyboardButton(text="👨‍💻 Обо мне", callback_data="about")],
        [InlineKeyboardButton(text="🤖 Разработка ботов", callback_data="category_bot")],
        [InlineKeyboardButton(text="🎨 Дизайн", callback_data="category_design")],
        [InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def portfolio_keyboard(category="all"):
    """Список проектов по категории"""
    if category == "bot":
        projects = BOT_PROJECTS
    elif category == "design":
        projects = DESIGN_PROJECTS
    else:
        projects = PORTFOLIO
    
    buttons = []
    for key, project in projects.items():
        emoji = "🤖" if project.get("category") == "bot" else "🎨"
        buttons.append([InlineKeyboardButton(
            text=f"{emoji} {project['name']}", 
            callback_data=f"project_{key}"
        )])
    
    # Кнопка назад в главное меню
    buttons.append([InlineKeyboardButton(text="🔙 На главную", callback_data="back_to_main")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def project_keyboard(project_key, project):
    """Клавиатура для конкретного проекта"""
    buttons = []
    
    # Кнопка заказа в зависимости от категории
    if project.get("category") == "design":
        buttons.append([InlineKeyboardButton(text="🎨 Заказать дизайн", url="https://t.me/shuga_dev")])
    else:
        buttons.append([InlineKeyboardButton(text="🤖 Заказать бота", url="https://t.me/shuga_dev")])
    
    # Кнопка назад в зависимости от категории
    if project.get("category") == "design":
        buttons.append([InlineKeyboardButton(text="🔙 К дизайн-проектам", callback_data="category_design")])
    else:
        buttons.append([InlineKeyboardButton(text="🔙 К разработке ботов", callback_data="category_bot")])
    
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def back_inline_keyboard():
    """Инлайн-кнопка 'Назад' на главную"""
    buttons = [[InlineKeyboardButton(text="🔙 На главную", callback_data="back_to_main")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# ----- ОБРАБОТЧИКИ КОМАНД -----
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """Приветствие с кнопкой 'Начать'"""
    text = (
        "<b>👋 Добро пожаловать!</b>\n\n"
        "Меня зовут <b>Лада</b>.\n\n"
        "Я <b>разработчик Telegram-ботов</b> и <b>дизайнер</b>.\n\n"
        "📌 <b>Чем могу быть полезна:</b>\n"
        "• 🤖 Разработка ботов для бизнеса\n"
        "• 🎨 Дизайн карточек товаров для маркетплейсов\n"
        "• 📱 Лендинги, дашборды, бренд-пакеты\n"
        "• 🔗 Комплексные решения: сайт + бот + дизайн\n\n"
        "<i>Нажмите кнопку «Начать», чтобы продолжить 👇</i>"
    )
    
    # Пробуем отправить фото, если есть
    avatar_path = BASE_DIR / "screens" / "avatar.jpg"
    if avatar_path.exists():
        try:
            photo = FSInputFile(avatar_path)
            await message.answer_photo(
                photo=photo, 
                caption=text, 
                reply_markup=start_keyboard()
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке аватара: {e}")
            await message.answer(text, reply_markup=start_keyboard())
    else:
        logger.warning(f"Аватар не найден: {avatar_path}")
        await message.answer(text, reply_markup=start_keyboard())

@dp.message(F.text == "🚀 Начать")
async def handle_start_button(message: types.Message):
    """Обработка нажатия кнопки 'Начать'"""
    text = (
        "<b>🏠 Главное меню</b>\n\n"
        "Выберите интересующий раздел 👇"
    )
    
    # Убираем Reply-клавиатуру
    await message.answer(
        text, 
        reply_markup=remove_keyboard()
    )
    
    # Показываем инлайн-меню
    await message.answer(
        text, 
        reply_markup=main_inline_keyboard()
    )

# ----- ОБРАБОТЧИКИ КАТЕГОРИЙ -----
@dp.callback_query(F.data == "category_bot")
async def show_bot_projects(callback: types.CallbackQuery):
    """Показать проекты по разработке ботов"""
    text = "<b>🤖 Мои проекты — Разработка ботов</b>\n\nВыберите проект, чтобы посмотреть детали:"
    
    try:
        await callback.message.edit_text(text, reply_markup=portfolio_keyboard("bot"))
    except Exception as e:
        logger.error(f"Ошибка при редактировании: {e}")
        await callback.message.answer(text, reply_markup=portfolio_keyboard("bot"))
    
    await callback.answer()

@dp.callback_query(F.data == "category_design")
async def show_design_projects(callback: types.CallbackQuery):
    """Показать дизайн-проекты"""
    text = "<b>🎨 Мои проекты — Дизайн</b>\n\nВыберите проект, чтобы посмотреть детали:"
    
    try:
        await callback.message.edit_text(text, reply_markup=portfolio_keyboard("design"))
    except Exception as e:
        logger.error(f"Ошибка при редактировании: {e}")
        await callback.message.answer(text, reply_markup=portfolio_keyboard("design"))
    
    await callback.answer()

# ----- ОБРАБОТЧИКИ КНОПОК -----
@dp.callback_query(F.data == "about")
async def about(callback: types.CallbackQuery):
    """Информация о разработчике"""
    text = (
        "<b>👨‍💻 Обо мне</b>\n\n"
        "<b>Чем занимаюсь:</b>\n"
        "• 🤖 Разработка Telegram-ботов различной сложности\n"
        "• 🎨 Дизайн карточек товаров для маркетплейсов\n"
        "• 📱 Лендинги, дашборды, бренд-пакеты\n"
        "• 🔗 Комплексные решения под ключ\n\n"
        
        "<b>Мой стек:</b>\n"
        "<b>Разработка:</b> Python / aiogram / SQLite / PostgreSQL\n"
        "<b>Дизайн:</b> Figma / Kandinsky / Canva / Photoshop\n\n"
        
        "<b>Почему я:</b>\n"
        "✅ Понимаю и разработку, и дизайн — ваши проекты будут реализуемы\n"
        "✅ Четкое соблюдение сроков\n"
        "✅ Поддержка после сдачи\n"
        "✅ Работаю через безопасную сделку"
    )
    
    try:
        await callback.message.edit_text(text, reply_markup=back_inline_keyboard())
    except Exception as e:
        logger.error(f"Ошибка в about: {e}")
        await callback.message.answer(text, reply_markup=back_inline_keyboard())
    
    await callback.answer()

@dp.callback_query(F.data.startswith("project_"))
async def show_project(callback: types.CallbackQuery):
    """Детали конкретного проекта с картинкой"""
    project_key = callback.data.replace("project_", "")
    
    # Ищем проект в обоих словарях
    project = BOT_PROJECTS.get(project_key) or DESIGN_PROJECTS.get(project_key)
    
    if not project:
        await callback.answer("Проект не найден", show_alert=True)
        return
    
    # Определяем эмодзи в зависимости от категории
    category_emoji = "🤖" if project.get("category") == "bot" else "🎨"
    
    # Формируем описание проекта
    text = (
        f"{category_emoji} <b>{project['name']}</b>\n\n"
        f"📝 <b>Описание:</b> {project['description']}\n\n"
        f"⚙️ <b>Технологии:</b> {project.get('tech', 'Не указано')}\n"
        f"⏱️ <b>Срок:</b> {project.get('duration', 'По запросу')}\n"
        f"💰 <b>Стоимость:</b> {project.get('price', 'Договорная')}\n\n"
        f"<i>Хотите такой же проект? Напишите мне!</i>"
    )
    
    # Получаем путь к картинке
    image_path = project.get("screens")
    
    if image_path:
        full_image_path = BASE_DIR / image_path
        
        if full_image_path.exists():
            try:
                photo = FSInputFile(full_image_path)
                await callback.message.answer_photo(
                    photo=photo,
                    caption=text,
                    reply_markup=project_keyboard(project_key, project)
                )
                await callback.answer("👍 Вот детали проекта")
            except Exception as e:
                logger.error(f"Ошибка при отправке картинки {full_image_path}: {e}")
                await callback.message.answer(text, reply_markup=project_keyboard(project_key, project))
        else:
            logger.warning(f"Файл {full_image_path} не найден")
            await callback.message.answer(text, reply_markup=project_keyboard(project_key, project))
    else:
        await callback.message.answer(text, reply_markup=project_keyboard(project_key, project))
    
    await callback.answer()

@dp.callback_query(F.data == "contacts")
async def contacts(callback: types.CallbackQuery):
    """Контакты"""
    text = (
        "<b>📞 Контакты</b>\n\n"
        "📱 <b>Telegram:</b> @shuga_dev\n"
        "📧 <b>Email:</b> ladashuga@mail.ru\n"
        "💼 <b>GitHub:</b> https://github.com/LadaShuga\n\n"
        "<i>Пишите, буду рада обсудить ваш проект!</i>"
    )
    
    try:
        await callback.message.edit_text(text, reply_markup=back_inline_keyboard())
    except Exception as e:
        logger.error(f"Ошибка в contacts: {e}")
        await callback.message.answer(text, reply_markup=back_inline_keyboard())
    
    await callback.answer()

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    """Возврат в главное меню"""
    text = "<b>🏠 Главное меню</b>\n\nВыберите интересующий раздел 👇"
    
    try:
        # Пробуем отредактировать существующее сообщение
        await callback.message.edit_text(text, reply_markup=main_inline_keyboard())
    except Exception as e:
        # Если не получилось отредактировать (нет текста для редактирования), отправляем новое
        logger.warning(f"Не удалось отредактировать сообщение: {e}")
        await callback.message.answer(text, reply_markup=main_inline_keyboard())
    
    await callback.answer()

# ----- ЗАПУСК БОТА -----
async def main():
    """Запуск бота"""
    print("🚀 Бот-визитка запущен!")
    print("=" * 50)
    
    # Принудительно удаляем вебхук и сбрасываем ожидающие обновления
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        print("✅ Вебхук удален, начинаем polling...")
    except Exception as e:
        print(f"⚠️ Ошибка при удалении вебхука: {e}")
    
    try:
        me = await bot.me()
        print(f"📱 Бот: @{me.username}")
    except:
        print("📱 Бот: (не удалось получить username)")
    
    print("\n📸 Проверка картинок в портфолио:")
    print("-" * 50)
    
    all_ok = True
    bot_count = 0
    design_count = 0
    
    # Проверяем проекты по разработке ботов
    print("\n🤖 Разработка ботов:")
    for key, project in BOT_PROJECTS.items():
        image_path = project.get("screens")
        if image_path:
            full_path = BASE_DIR / image_path
            if full_path.exists():
                print(f"  ✅ {project['name']}")
                bot_count += 1
            else:
                print(f"  ❌ {project['name']}: ФАЙЛ НЕ НАЙДЕН! {full_path}")
                all_ok = False
        else:
            print(f"  ⚠️ {project['name']}: путь к картинке не указан")
            all_ok = False
    
    # Проверяем дизайн-проекты
    print("\n🎨 Дизайн:")
    for key, project in DESIGN_PROJECTS.items():
        image_path = project.get("screens")
        if image_path:
            full_path = BASE_DIR / image_path
            if full_path.exists():
                print(f"  ✅ {project['name']}")
                design_count += 1
            else:
                print(f"  ❌ {project['name']}: ФАЙЛ НЕ НАЙДЕН! {full_path}")
                all_ok = False
        else:
            print(f"  ⚠️ {project['name']}: путь к картинке не указан")
            all_ok = False
    
    print("\n" + "-" * 50)
    print(f"📊 Итого: {bot_count} проектов по разработке, {design_count} дизайн-проектов")
    
    if not all_ok:
        print("\n⚠️  ВНИМАНИЕ: Некоторые картинки не найдены!")
        print("Проверьте пути в portfolio.py и наличие файлов в папке screens/")
    else:
        print("\n✅ Все картинки найдены!")
    
    # Проверяем наличие аватара
    avatar_path = BASE_DIR / "screens" / "avatar.jpg"
    if avatar_path.exists():
        print("\n✅ Аватар найден!")
    else:
        print("\n⚠️ Аватар не найден: screens/avatar.jpg")
    
    print("\n" + "=" * 50)
    print("🎉 Бот готов к работе!")
    print("=" * 50)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n❌ Бот остановлен")
