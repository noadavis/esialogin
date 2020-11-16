### Устанавливаем Крипто про и настраиваем подпись

Что необходимо собрать до начала:
> Папка контейнера эцп гост2012 с 6ю файлами: header.key, masks2.key, masks.key, name.key, primary2.key, primary.key

> Необходимо знать имя контейнера, можно посмотреть в файле name.key

> Открытый ключ контейнера в base64 формате

> Корневые сертификаты крипто про: cacer.p7b, wget http://cpca.cryptopro.ru/cacer.p7b

> Установщик крипто про csp 4.0: linux-amd64_deb.tgz

Переменные:
> CONTAINER_DIR: Папка контейнера

> CONTAINER_NAME: Имя контейнера

> PUBLIK_KEY.CRT: Открытый ключ

> dev: логин пользователя linux, с правами которого запускается сервис esialogin

### Устанавливаем крипто про
```bash
tar -xf linux-amd64_deb.tgz
cd linux-amd64_deb
chmod +x install.sh
sudo ./install.sh
```

### Желательно проверить наличие симлинков в каталоге /usr/local/bin и если их нет, то создать
```bash
cd /usr/local/bin
sudo ln -s /opt/cprocsp/bin/amd64/certmgr
sudo ln -s /opt/cprocsp/bin/amd64/cpverify
sudo ln -s /opt/cprocsp/bin/amd64/cryptcp
sudo ln -s /opt/cprocsp/bin/amd64/csptest
sudo ln -s /opt/cprocsp/bin/amd64/csptestf
sudo ln -s /opt/cprocsp/bin/amd64/der2xer
sudo ln -s /opt/cprocsp/bin/amd64/inittst
sudo ln -s /opt/cprocsp/bin/amd64/wipefile
sudo ln -s /opt/cprocsp/sbin/amd64/cpconfig
```

### Просмотр и установка текущий лицензии
```bash
/opt/cprocsp/sbin/amd64/cpconfig -license -view
sudo /opt/cprocsp/sbin/amd64/cpconfig -license -set <серийный_номер>
```

### Устанавливаем корневые сертификаты
```bash
sudo /opt/cprocsp/bin/amd64/certmgr -inst -all -store uroot -file cacer.p7b
```

### Копируем контейнер в директорию с ключами, даем права пользователю сервиса
Итоговая директория контейнера должна быть вида /var/opt/cprocsp/keys/<логин пользователя системы>/<папка контейнера>/
```bash
sudo mkdir /var/opt/cprocsp/keys/dev/
sudo cp -r /home/dev/crypto/<CONTAINER_DIR>/ /var/opt/cprocsp/keys/dev/
sudo chown -R dev:dev /var/opt/cprocsp/keys/dev/
```

### Проверяем правильность установки контейнера, проверяем его наличие в списке и запоминаем его имя
Запускать команду необходимо пользователем dev
```bash
/opt/cprocsp/bin/amd64/csptest -keyset -enum_cont -verifycontext -fqcn
```
```bash
dev@esialogin:~$ /opt/cprocsp/bin/amd64/csptest -keyset -enum_cont -verifycontext -fqcn
CSP (Type:80) v4.0.9019 KC1 Release Ver:4.0.9963 OS:Linux CPU:AMD64 FastCode:READY:AVX.
AcquireContext: OK. HCRYPTPROV: 33728435
\\.\HDIMAGE\<CONTAINER_NAME>
OK.
Total: SYS: 0.000 sec USR: 0.010 sec UTC: 0.080 sec
[ErrorCode: 0x00000000]
```

### Связываем открытый ключ PUBLIK_KEY.CRT с контейнером
Запускать команду необходимо пользователем dev
```bash
/opt/cprocsp/bin/amd64/certmgr -inst -file /home/dev/crypto/<PUBLIK_KEY.CRT> -cont '\\.\HDIMAGE\<CONTAINER_NAME>'
```

### Проверяем наличие связи и запоминаем SHA1 Hash
```bash
/opt/cprocsp/bin/amd64/certmgr --list
```
```bash
...
SHA1 Hash           : <...>
PrivateKey Link     : Yes
Container           : HDIMAGE\\.....
...
```
