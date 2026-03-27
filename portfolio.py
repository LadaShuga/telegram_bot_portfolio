# portfolio.py

PORTFOLIO = {
    "parser": {
        "name": "⚡️ Бот-парсер вакансий на hh.ru",
        "description": "Собирает данные с сайта hh.ru о вакансиях. Можно ознакомиться с ним по ссылке: @freelance_hunter_parser_bot",
        "tech": "Python, aiogram, sqlite, scheduler",
        "screens": "screens/hhparse.png",
        "price": "от 5 000 ₽",
        "duration": "1 неделя"
    },
    "booking": {
        "name": "📊 Бот для записи в салон красоты",
        "description": "Бот предназначен для онлайн-записи в салон красоты. Можно ознакомиться с ним по ссылке: @TestBookingbot_bot",
        "tech": "Python, aiogram, sqlite, apscheduler",
        "screens": "screens/bron.png",
        "price": "от 10 000 ₽",
        "duration": "1 неделя"
    },
    "card_infographic": {
        "name": "🛍 Карточка товара | Инфографика",
        "description": "Техничная карточка с акцентом на характеристики: размерная сетка, состав, уход. Идеально для товаров с четкими параметрами.",
        "tech": "Figma, Supa, QWEN",
        "screens": "screens/skirt.png", 
        "price": "от 500 ₽/карточка",
        "duration": "от 1 часа",
        "category": "design"
    },
    "brand_pack": {
        "name": "🎨 Бренд-пакет для кофейни",
        "description": "<Бренд-пакет для кофейни - логотип, мокапы, макет визитки",
        "tech": "Kandinsky, QWEN, , Supa, Figma",
        "screens": "screens/coffee.png",
        "price": "от 2 000 ₽",
        "duration": "1-2 дня",
        "category": "design"
    },
    "card-sale": {
        "name": "📱 Карточка товара",
        "description": "Продающий лендинг для школы программирования. Адаптив под мобильные, форма записи, интеграция с Telegram-ботом.",
        "tech": "Figma, QWEN, Supa",
        "screens": "screens/dress.png", 
        "price": "от 500 ₽/карточка",
        "duration": "от 1 часа",
        "category": "design"
    }
}

# Объединяем для обратной совместимости (если где-то используется PORTFOLIO)
PORTFOLIO = {**BOT_PROJECTS, **DESIGN_PROJECTS}

# Функции для работы с категориями
def get_projects_by_category(category=None):
    """Возвращает проекты по категории (bot/design/all)"""
    if category == "bot":
        return BOT_PROJECTS
    elif category == "design":
        return DESIGN_PROJECTS
    else:
        return PORTFOLIO

def get_categories():
    """Возвращает список категорий"""
    return [
        {"id": "bot", "name": "🤖 Разработка ботов", "emoji": "🤖"},
        {"id": "design", "name": "🎨 Дизайн", "emoji": "🎨"}
    ]

def get_portfolio():
    """Возвращает список проектов для портфолио (для обратной совместимости)"""
    projects = []
    for key, project in PORTFOLIO.items():
        projects.append({
            "title": project["name"],
            "description": project["description"],
            "photo": project["screens"],
            "technologies": project["tech"],
            "price": project["price"],
            "duration": project["duration"],
            "key": key,
            "category": project.get("category", "bot")
        })
    return projects
