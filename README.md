## Установка

Клонировать репозиторий
```bash
git clone https://github.com/kzadm/azhar.git
```

Перейти в папку с проектом
```bash
cd some-project-folder
```

Установка виртуального окружения python
```bash
python3 -m venv venv
```

Активация виртуального окружения Windows
```bash
.\venv\Scripts\activate.bat
```

Активация виртуального окружения Linux
```bash
source venv/bin/activate
```

Установка зависимостей проекта
```bash
pip install -r requirements.txt
```

Выполить миграции базы данных
```bash
python manage.py migrate
```

Создать Администратора для доступа к админ панели (после ввода данной команды следовать инструкциям - ввести логин админа и пароль (должен содержать не менее 8 символов), почта не обязательно)
```bash
python manage.py createsuperuser
```

**Чтобы добавить фейковых студентов (не обязательно), нужно сначала войти в админ панель и создать по крайней мере ОДНУ СПЕЦИАЛЬНОСТЬ и ДВЕ КВАЛИФИКАЦИИ** затем выполнить команду
```bash
python create_students.py
```

Запуск проекта
```bash
python manage.py runserver
```

Далее проект будет доступен по адресу [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

Производим вход