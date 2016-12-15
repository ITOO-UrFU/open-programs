# open-programs

## Установка
1. Установить Python 3
2. Установить `virtualenv`:

    `$ pip3 install virtualenv`

3. Перейдите в папку, где будет храниться проект
4. Создать виртуальное окружение в данной папке:

    `$ virtualenv env`

5. Активируем виртуальное окружение

    `$ . env/bin/activate` или `$ source env/bin/activate`

6. Склонируйте git репозиторий

    `git clone https://github.com/ITOO-UrFU/open-programs.git`

7. Перейти в папку `open-programs` и установить зависимости

    `$ pip install -r requirements.txt`

## Запуск сервера

`$ ./manage.py migrate`

`$ ./manage.py compilemessages`

`$ ./manage.py runserver`

## Создание суперпользователя

`$ ./manage.py addroot <username>`
