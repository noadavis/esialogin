#<CONTAINER_DIR>: Папка контейнера, содержащая шесть файлов
#<CONTAINER_NAME>: Имя контейнера
#<PUBLIK_KEY.CRT>: Файл открытого ключа
#В папке esialogin/crypto должны находиться файлы: linux-amd64_deb.tgz, <PUBLIK_KEY.CRT>, <CONTAINER_DIR>

FROM ubuntu:20.04
#enviroment options
ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"]

#system requirements
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y nano net-tools python3-pip zip unzip wget git virtualenv build-essential python3-dev
#postgresql при необходимости
RUN apt-get install -y libpq-dev
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

#service user
RUN addgroup -gid 1000 dev
RUN useradd -ms /bin/bash dev -u 1000 -g 1000
RUN echo "dev:dev" | chpasswd
RUN adduser dev sudo
USER dev

RUN pip3 install uWSGI daemonize Django django-settings-json
#postgresql при необходимости
RUN pip3 install psycopg2 psycopg2-binary

#signature prepare
RUN mkdir /home/dev/crypto/
WORKDIR /home/dev/crypto/
COPY crypto/linux-amd64_deb.tgz ./

#crypto pro install
RUN tar -xf linux-amd64_deb.tgz
WORKDIR /home/dev/crypto/linux-amd64_deb/
RUN chmod +x install.sh
USER root
RUN ./install.sh
WORKDIR /usr/local/bin
RUN ln -s /opt/cprocsp/bin/amd64/certmgr
RUN ln -s /opt/cprocsp/bin/amd64/cpverify
RUN ln -s /opt/cprocsp/bin/amd64/cryptcp
RUN ln -s /opt/cprocsp/bin/amd64/csptest
RUN ln -s /opt/cprocsp/bin/amd64/csptestf
RUN ln -s /opt/cprocsp/bin/amd64/der2xer
RUN ln -s /opt/cprocsp/bin/amd64/inittst
RUN ln -s /opt/cprocsp/bin/amd64/wipefile
RUN ln -s /opt/cprocsp/sbin/amd64/cpconfig

#signature install
WORKDIR /home/dev/crypto/
COPY crypto/<PUBLIK_KEY.CRT> ./
RUN wget http://cpca.cryptopro.ru/cacer.p7b
RUN yes o | /opt/cprocsp/bin/amd64/certmgr -inst -all -store uroot -file cacer.p7b
RUN mkdir /var/opt/cprocsp/keys/dev/
WORKDIR /var/opt/cprocsp/keys/dev/
COPY crypto/<CONTAINER_DIR> ./
RUN chown -R dev:dev /var/opt/cprocsp/keys/dev/
USER dev
RUN /opt/cprocsp/bin/amd64/csptest -keyset -enum_cont -verifycontext -fqcn
RUN /opt/cprocsp/bin/amd64/certmgr -inst -file /home/dev/crypto/<PUBLIK_KEY.CRT> -cont '\\.\HDIMAGE\<CONTAINER_NAME>'

RUN /opt/cprocsp/bin/amd64/certmgr --list

#service install
USER root
WORKDIR /home/dev/esialogin/
COPY . ./
RUN chown -R dev:dev /home/dev/esialogin/
USER dev

ENTRYPOINT python manage.py runserver 0.0.0.0:9999
