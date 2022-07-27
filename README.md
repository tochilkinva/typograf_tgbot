# typograf_tgbot
Telegram bot with Typograf service

### Описание
Telegram-бот, который использует сервис Типограф для правки текста.   
https://www.artlebedev.ru/typograf/

### Команды
- /start - Появляется при первом старте бота
- /help - Выводит 2 примера в виде кнопок 
- Любой текст - отправляет текст в сервис Типограф и возвращает исправленный

### Технологии
Python 3.7.9, aiogram, remotetypograf

### Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/tochilkinva/typograf_tgbot.git
cd typograf_tgbot
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
. env/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Создайте файл .env и укажите необходимые данные.
Пример есть в env_example.txt.
Затем просто запустите код main.py в Python.

### Автор
Валентин
