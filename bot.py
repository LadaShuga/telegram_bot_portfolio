import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# Наши локальные файлы
from config import BOT_TOKEN, ADMIN_IDS
from portfolio import PORTFOLIO

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ----- КЛАВИАТУРЫ -----
def main_keyboard():
    """Главное меню"""
    buttons = [
        [InlineKeyboardButton(text="👨‍💻 Обо мне", callback_data="about")],
        [InlineKeyboardButton(text="📂 Портфолио", callback_data="portfolio")],
        [InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def portfolio_keyboard():
    """Список проектов"""
    buttons = []
    for key, project in PORTFOLIO.items():
        buttons.append([InlineKeyboardButton(text=project["name"], callback_data=f"project_{key}")])
    buttons.append([InlineKeyboardButton(text="🔙 На главную", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def project_keyboard(project_key):
    """Клавиатура для конкретного проекта"""
    buttons = [
        [InlineKeyboardButton(text="📨 Заказать такой же", url="https://t.me/lada_pieceof_hell")],  # Замените на свой
        [InlineKeyboardButton(text="🔙 К списку проектов", callback_data="back_to_portfolio")],  # Изменено!
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def back_keyboard():
    """Кнопка 'Назад' на главную"""
    buttons = [[InlineKeyboardButton(text="🔙 На главную", callback_data="back_to_main")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# ----- ОБРАБОТЧИКИ КОМАНД -----
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Приветствие"""
    text = (
        "<b>👋 Привет! Меня зовут Лада и я разработчик Telegram-ботов</b>\n\n"
        "Создаю профессиональные боты для бизнеса и не только.\n"
        "В портфолио - реальные проекты с примерами работ.\n\n"
        "<i>Выберите интересующий раздел:</i>"
    )
    
    # Пробуем отправить фото, если есть
    try:
        photo = types.FSInputFile("portfolio/telegram_bot_portfolio/screens/avatar.jpg")
        await message.answer_photo(photo=photo, caption=text, reply_markup=main_keyboard())
    except:
        await message.answer(text, reply_markup=main_keyboard())

    
# ----- ОБРАБОТЧИКИ КНОПОК -----
@dp.callback_query(F.data == "about")
async def about(callback: types.CallbackQuery):
    """Информация о разработчике"""
    text = (
        "<b>👨‍💻 Обо мне</b>\n\n"
        "<b>Чем занимаюсь:</b>\n"
        "• Разработка Telegram ботов различной сложности\n"
        "• Парсинг данных и автоматизация\n"
        "• Системы бронирования и записи\n"
        "• Интеграция с базами данных\n\n"
        
        "<b>Мой стек:</b>\n"
        "• Python / aiogram\n"
        "• SQLite / PostgreSQL\n"
        "• Парсинг (BeautifulSoup, Selenium)\n"
        "• Планировщики задач (APScheduler)\n\n"
        
        "<b>Могу создать шаблон/референс графического наполнения</b> \n"
        
        "<b>Почему Я?:</b>\n"
        "✅ Четкое соблюдение сроков\n"
        "✅ Понятная документация\n"
        "✅ Поддержка после сдачи"
    )
    
    # ВАЖНО: Проверяем тип сообщения
    try:
        if callback.message.photo:
            # Если это сообщение с фото - отправляем новое текстовое
            await callback.message.answer(text, reply_markup=back_keyboard())
        else:
            # Если это текстовое - редактируем
            await callback.message.edit_text(text, reply_markup=back_keyboard())
    except Exception as e:
        # Если ошибка - отправляем новое сообщение
        print(f"Ошибка в about: {e}")
        await callback.message.answer(text, reply_markup=back_keyboard())
    
    await callback.answer()

@dp.callback_query(F.data == "portfolio")
async def show_portfolio(callback: types.CallbackQuery):
    """Список проектов"""
    text = "<b>📂 Мои проекты</b>\n\nВыберите проект, чтобы посмотреть детали и примеры работ:"
    
    # Проверяем тип сообщения
    if callback.message.photo:
        # Если это сообщение с фото - отправляем новое текстовое
        await callback.message.answer(text, reply_markup=portfolio_keyboard())
    else:
        # Если это текстовое - редактируем
        await callback.message.edit_text(text, reply_markup=portfolio_keyboard())
    
    await callback.answer()

@dp.callback_query(F.data == "back_to_portfolio")  # НОВЫЙ ОБРАБОТЧИК!
async def back_to_portfolio(callback: types.CallbackQuery):
    """Возврат к списку проектов (специально для сообщений с фото)"""
    text = "<b>📂 Мои проекты</b>\n\nВыберите проект, чтобы посмотреть детали и примеры работ:"
    
    # Всегда отправляем новое сообщение, чтобы не запутаться с типами
    await callback.message.answer(text, reply_markup=portfolio_keyboard())
    await callback.answer("👆 Список проектов")

@dp.callback_query(F.data.startswith("project_"))
async def show_project(callback: types.CallbackQuery):
    """Детали конкретного проекта с картинкой"""
    project_key = callback.data.replace("project_", "")
    project = PORTFOLIO.get(project_key)
    
    if not project:
        await callback.answer("Проект не найден", show_alert=True)
        return
    
    # Формируем описание проекта
    text = (
        f"<b>{project['name']}</b>\n\n"
        f"📝 <b>Описание:</b> {project['description']}\n\n"
        f"⚙️ <b>Технологии:</b> {project.get('tech', 'Не указано')}\n"
        f"⏱️ <b>Срок разработки:</b> {project.get('duration', 'По запросу')}\n"
        f"💰 <b>Стоимость:</b> {project.get('price', 'Договорная')}\n\n"
        f"<i>Хотите такой же бот? Напишите мне!</i>"
    )
    
    # Получаем путь к картинке
    image_path = project.get("screens")
    
    if image_path and os.path.exists(image_path):
        try:
            # Отправляем новое сообщение с фото
            photo = types.FSInputFile(image_path)
            
            await callback.message.answer_photo(
                photo=photo,
                caption=text,
                reply_markup=project_keyboard(project_key)
            )
            
            await callback.answer("👍 Вот детали проекта")
            
        except Exception as e:
            print(f"Ошибка при отправке картинки: {e}")
            # Если ошибка с картинкой, показываем текст
            await callback.message.answer(text, reply_markup=project_keyboard(project_key))
            await callback.answer()
    else:
        # Если картинки нет - отправляем текст
        if image_path and not os.path.exists(image_path):
            print(f"Файл {image_path} не найден")
        
        await callback.message.answer(text, reply_markup=project_keyboard(project_key))
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
    
    if callback.message.photo:
        await callback.message.answer(text, reply_markup=back_keyboard())
    else:
        await callback.message.edit_text(text, reply_markup=back_keyboard())
    
    await callback.answer()

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    """Возврат в главное меню"""
    text = "<b>🏠 Главное меню</b>\n\nЧем я могу вам помочь?"
    
    if callback.message.photo:
        await callback.message.answer(text, reply_markup=main_keyboard())
    else:
        await callback.message.edit_text(text, reply_markup=main_keyboard())
    
    await callback.answer()

# ----- ЗАПУСК БОТА -----
async def main():
    """Запуск бота"""
    print("🚀 Бот-визитка запущен!")
    print("=" * 40)
    
    try:
        me = await bot.me()
        print(f"📱 Бот: @{me.username}")
    except:
        print("📱 Бот: (не удалось получить username)")
    
    print("\n📸 Проверка картинок в портфолио:")
    all_ok = True
    
    for key, project in PORTFOLIO.items():
        image_path = project.get("screens")
        if image_path:
            if os.path.exists(image_path):
                print(f"  ✅ {project['name']}: {image_path}")
            else:
                print(f"  ❌ {project['name']}: ФАЙЛ НЕ НАЙДЕН! {image_path}")
                all_ok = False
        else:
            print(f"  ⚠️ {project['name']}: путь к картинке не указан")
            all_ok = False
    
    if not all_ok:
        print("\n⚠️  ВНИМАНИЕ: Некоторые картинки не найдены!")
        print("Проверьте пути в portfolio.py и наличие файлов в папке screens/")
    else:
        print("\n✅ Все картинки найдены!")
    
    print("\n" + "=" * 40)
    print("🎉 Бот готов к работе!")
    print("=" * 40)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n❌ Бот остановлен")