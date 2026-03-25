import os
import logging
from pathlib import Path
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from portfolio import get_portfolio

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Получаем абсолютный путь к папке со скриптом
BASE_DIR = Path(__file__).parent

# Берем токен из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    logger.error("BOT_TOKEN не найден в переменных окружения!")
    exit(1)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    """Обработчик команды /start"""
    await message.answer(
        "👋 Привет! Я бот-портфолио.\n\n"
        "📁 Используй /portfolio чтобы посмотреть мои работы.\n"
        "💼 Здесь собраны все мои проекты с описаниями и скриншотами.\n\n"
        "💰 Также я могу рассчитать стоимость и сроки разработки.\n"
        "Просто напиши, какой проект тебя заинтересовал!"
    )
    logger.info(f"Пользователь {message.from_user.id} запустил бота")


@dp.message(Command("portfolio"))
async def portfolio(message: types.Message):
    """Обработчик команды /portfolio - показывает все проекты"""
    try:
        # Получаем список проектов из portfolio.py
        projects = get_portfolio()
        
        if not projects:
            await message.answer("❌ Проекты не найдены.")
            logger.warning("Список проектов пуст")
            return
        
        # Отправляем приветственное сообщение
        await message.answer(
            f"📁 Всего проектов: {len(projects)}\n\n"
            "⬇️ Вот мои работы:"
        )
        
        # Отправляем каждый проект
        for idx, project in enumerate(projects, 1):
            # Формируем текст проекта
            text = (
                f"*{idx}. {project['title']}*\n\n"
                f"📝 {project['description']}\n\n"
                f"🔧 *Технологии:* {project['technologies']}\n"
                f"💰 *Стоимость:* {project['price']}\n"
                f"⏱ *Срок:* {project['duration']}"
            )
            
            # Проверяем наличие фото
            if project.get('photo'):
                # Формируем полный путь к файлу
                photo_path = BASE_DIR / "screens" / project['photo']
                
                if photo_path.exists():
                    try:
                        # Отправляем фото с подписью
                        photo_file = FSInputFile(photo_path)
                        await message.answer_photo(
                            photo_file,
                            caption=text,
                            parse_mode="Markdown"
                        )
                        logger.info(f"Отправлен проект {idx}: {project['title']} с фото {project['photo']}")
                    except Exception as e:
                        logger.error(f"Ошибка при отправке фото {photo_path}: {e}")
                        await message.answer(
                            text + "\n\n❌ Не удалось загрузить фото",
                            parse_mode="Markdown"
                        )
                else:
                    logger.warning(f"Фото не найдено: {photo_path}")
                    await message.answer(
                        text + "\n\n❌ Фото временно недоступно",
                        parse_mode="Markdown"
                    )
            else:
                # Если фото нет, отправляем только текст
                await message.answer(text, parse_mode="Markdown")
                logger.info(f"Отправлен проект {idx}: {project['title']} (без фото)")
        
        # Отправляем завершающее сообщение
        await message.answer(
            "✅ Все проекты показаны!\n\n"
            "💬 Если вас заинтересовал какой-то проект, "
            "напишите /contact для связи со мной!"
        )
        
    except Exception as e:
        logger.error(f"Ошибка при отправке портфолио: {e}")
        await message.answer(
            "❌ Произошла ошибка при загрузке портфолио.\n"
            "Попробуйте позже или обратитесь к администратору."
        )


@dp.message(Command("contact"))
async def contact(message: types.Message):
    """Обработчик команды /contact"""
    await message.answer(
        "📱 *Связаться со мной:*\n\n"
        "✉️ Email: ladashuga@mail.ru\n"
        "💬 Telegram:@shuga_dev\n"
        "📱 Phone: +7 (964) 469-16-50\n\n"
        "💼 GitHub: https://github.com/LadaShuga\n\n"
        "Буду рад ответить на ваши вопросы! 🤝",
        parse_mode="Markdown"
    )


@dp.message()
async def handle_unknown(message: types.Message):
    """Обработчик неизвестных команд"""
    await message.answer(
        "🤔 Я не понимаю эту команду.\n\n"
        "Используйте:\n"
        "/start - приветствие\n"
        "/portfolio - посмотреть портфолио\n"
        "/contact - связаться со мной"
    )


if __name__ == '__main__':
    logger.info("Бот запущен и готов к работе!")
    dp.run_polling(bot)
