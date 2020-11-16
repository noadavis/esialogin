### Настройка конфига системы
```bash
//Запускать django в debug режиме
"DEBUG": true,
//Использовать postgresql? иначе будет использоваться sqlite3
"USE_POSTGRESQL": false,
//Доступ к postgresql серверу, только при "USE_POSTGRESQL": true
"DB_NAME": "db_name",
"DB_USER": "db_user",
"DB_PASSWORD": "db_user_password",
"DB_HOST": "db_ip",
"DB_PORT": 5432,
//Пароль к контейнеру цифровой подписи
"SIGN_PASSWORD": "SIGN_PASSWORD",
//Sha1 открытого ключа
"SHA1_PUBLIC_KEY": "SHA1_PUBLIC_KEY",
//Адрес системы, используется для формирования есиа redirect_uri 
"SYSTEM_URL": "http://127.0.0.1:9999",
//Какую информацию запрашивать, fullname snils необходимы для работы сервиса, scope заполняются через пробел
"ESIA_SCOPE": "fullname snils",
//Зарегистрированный в есиа client_id
"ESIA_CLIENT_ID": "ESIA_CLIENT_ID",
//Обращатся к тестовуми порталу есиа?
"ESIA_TEST": true
```
