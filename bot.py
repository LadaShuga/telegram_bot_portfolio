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
        "💼 Здесь собраны все мои проекты с описаниями и скриншотами."
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
            text = f"*{idx}. {project['title']}*\n\n{project['description']}"
            
            # Добавляем технологии, если есть
            if project.get('technologies'):
                tech_str = ", ".join(project['technologies'])
                text += f"\n\n🔧 *Технологии:* {tech_str}"
            
            # Добавляем ссылку, если есть
            if project.get('link'):
                text += f"\n\n🔗 [Ссылка на проект]({project['link']})"
            
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
            "Спасибо за внимание! 🙌"
        )
        
    except Exception as e:
        logger.error(f"Ошибка при отправке портфолио: {e}")
        await message.answer(
            "❌ Произошла ошибка при загрузке портфолио.\n"
            "Попробуйте позже или обратитесь к администратору."
        )


@dp.message()
async def handle_unknown(message: types.Message):
    """Обработчик неизвестных команд"""
    await message.answer(
        "🤔 Я не понимаю эту команду.\n\n"
        "Используйте:\n"
        "/start - приветствие\n"
        "/portfolio - посмотреть портфолио"
    )


if __name__ == '__main__':
    logger.info("Бот запущен и готов к работе!")
    dp.run_polling(bot)
