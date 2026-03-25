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
    }
}

def get_portfolio():
    """Возвращает список проектов для портфолио в виде списка словарей"""
    projects = []
    for key, project in PORTFOLIO.items():
        projects.append({
            "title": project["name"],
            "description": project["description"],
            "photo": project["screens"],
            "technologies": project["tech"],
            "price": project["price"],
            "duration": project["duration"],
            "key": key
        })
    return projects
