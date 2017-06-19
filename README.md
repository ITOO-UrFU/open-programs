# open-programs

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/04e518824fa34be2b98e7bc3ae14e428)](https://www.codacy.com/app/mastergowen/open-programs?utm_source=github.com&utm_medium=referral&utm_content=ITOO-UrFU/open-programs&utm_campaign=badger)

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

## Разное

Для работы с accdb загрузить драйвер:

`https://www.microsoft.com/en-US/download/details.aspx?id=13255`
