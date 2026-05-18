## Шаги по запуску:
1) Установть RabbitMQ на ПК и предварительно запустить его.
2) После открытия проекта в IDE, нужно перейти в папку:
```cmd
cd myproject
```
3) Установить пакеты:
```shell
pip install -r requirements.txt
```
4) Открыть 3 терминала
   - В первом терменале прописать: `celery -A myproject worker --loglevel=info -P solo` (сам воркер)
   - Во втором теримнале прописать: `celery -A myproject beat --loglevel=info`
   - В третьем просто запустить проект: `python manage.py runserver`
