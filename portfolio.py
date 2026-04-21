# portfolio.py

# ========== РАЗРАБОТКА БОТОВ ==========
BOT_PROJECTS = {
    "parser": {
        "name": "Бот-парсер вакансий на hh.ru",
        "description": "Собирает данные с сайта hh.ru о вакансиях. Можно ознакомиться с ним по ссылке: @freelance_hunter_parser_bot",
        "tech": "Python, aiogram, sqlite, scheduler",
        "screens": "screens/hhparse.png",
        "price": "от 5 000 ₽",
        "duration": "1 неделя",
        "category": "bot"
    },
    "booking": {
        "name": "Бот для записи в салон красоты",
        "description": "Бот предназначен для онлайн-записи в салон красоты. Можно ознакомиться с ним по ссылке: @TestBookingbot_bot",
        "tech": "Python, aiogram, sqlite, apscheduler",
        "screens": "screens/bron.png",
        "price": "от 10 000 ₽",
        "duration": "1 неделя",
        "category": "bot"
    }
}

# ========== ДИЗАЙН-ПРОЕКТЫ ==========
DESIGN_PROJECTS = {
    "card_infographic": {
        "name": "Карточка товара | Инфографика",
        "description": "Техничная карточка с акцентом на характеристики: размерная сетка, состав, уход. Идеально для товаров с четкими параметрами.",
        "tech": "Figma, Supa, QWEN",
        "screens": "screens/ДЗ 3.png", 
        "price": "от 500 ₽/карточка",
        "duration": "от 1 часа",
        "category": "design"
    },
    "brand_pack": {
        "name": "Запретграмм-пост для NFT-магазина",
        "description": "Запретграмм-пост для NFT-магазина",
        "tech": "QWEN, Figma",
        "screens": "screens/Instarfam post - 1.png",
        "price": "от 2 000 ₽",
        "duration": "1-2 дня",
        "category": "design"
    },
    "card_sale": {
        "name": "Карточка товара | Lifestyle",
        "description": "Яркая карточка товара с акцентом на продажи. Адаптив под мобильные, акцент на цену и преимущества.",
        "tech": "Figma, QWEN, Supa",
        "screens": "screens/.png", 
        "price": "от 500 ₽/карточка",
        "duration": "от 1 часа",
        "category": "design"
    },
    "kvn_posters": {
        "name": "Афиши КВН | Серия работ",
        "description": "Серия афиш для игр и фестивалей КВН. В работе использованы: яркие цвета, динамичная композиция, фотоколлаж. Задача — привлечь зрителей и передать атмосферу праздника.",
        "tech": "Photoshop, Figma, Supa",
        "screens": [
            "screens/kvn1.png",
            "screens/kvn2.png",
            "screens/kvn3.png",
            "screens/logo_kvn.png"
        ],
        "price": "от 1 000 ₽",
        "duration": "1-2 дня",
        "category": "design",
        "is_album": True
    }
}

# Объединяем все проекты в один словарь для обратной совместимости
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
