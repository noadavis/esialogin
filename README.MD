### ESIA OAUTH2 CRYPTOPRO GOST2012

Пример авторизации через сервис ЕСИА методом OAUTH2 с подписью GOST2012, подписание через Крипто про CSP 4
> Django3.1, Python3.8, Crypto pro CSP 4.0, авторизация без библиотек oauth

Реализация:
> Реализация oauth2 авторизации: [esialogin/apps/esia/views.py](esialogin/apps/esia/views.py)

> Подписание крипто про: [esialogin/apps/crypto/models.py](esialogin/apps/crypto/models.py)

> Получение информации из есиа: [esialogin/apps/login/views.py](esialogin/apps/login/views.py):esia(request)

### Запуск сервиса
```bash
$ source ~/venv/bin/activate
$ cd /home/dev/esialogin/
$ python manage.py runserver 127.0.0.1:9999
```

### Сборка системы на ubuntu server 20.04
Пользователь системы: dev

### Настройка системы
```bash
$ apt update
$ apt upgrade
# Библиотеки для виртуального окружения python3
$ apt install virtualenv build-essential python3-dev
# Библиотека для поддержки postgresql, при необходимости
$ apt install libpq-dev
# Установим python3 по умолчанию
$ update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1
```

### Настраиваем виртуальное окружение python
```bash
$ cd /home/dev/
$ virtualenv -p python3 venv
$ source ~/venv/bin/activate
$ pip3 install uWSGI daemonize Django django-settings-json
# Библиотека для поддержки postgresql, при необходимости
$ pip3 install psycopg2 psycopg2-binary
```

### Устанавливаем Крипто про и настраиваем подпись
[Инструкция: CRYPTOPRO.MD](CRYPTOPRO.MD)

### Получаем сервис
```bash
# Получаем и настраиваем сервис
$ git clone https://github.com/noadavis/esialogin.git
$ cd /home/dev/esialogin/
```

### Настраиваем конфиг сервиса
[Инструкция: SETTINGS.MD](SETTINGS.MD)
```bash
$ cp esialogin/settings.json.basic esialogin/settings.json
$ nano esialogin/settings.json
```

### Перед первым запуском 
```bash
# Применяем миграции базы данных
$ python manage.py migrate

# Создадим пользователя для проверки системы, без авторизации есиа
$ python manage.py createuser --login user --password 123

# Проверим правильность настройки крипто про и работы модуля подписания
$ python manage.py signtest --sign test_message
```

### Запускаем сервис
```bash
$ python manage.py runserver 127.0.0.1:9999
```

### BASH ALIAS
```bash
alias venv="source /home/dev/venv/bin/activate; cd /home/dev/esialogin;"
alias envupd="pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U"
```

### Bootstrap 4
В проекте используется тема для bootstrap 4: [vali-admin](https://github.com/pratikborsadiya/vali-admin)
