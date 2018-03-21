from flask import Flask, render_template
import datetime
from cache import *
from urllib.request import urlopen
from xml.etree import ElementTree as etree

app = Flask(__name__)


@app.route('/')
@Cached()
def hello():
    # Приводим дату к нужному формату
    d = datetime.datetime.today().strftime('%d/%m/%Y')
    # Приводим источники к нужному формату
    cur = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={d}'
    met = f'https://www.cbr.ru/scripts/xml_metall.asp?date_req1={d}&date_req2={d}'
    # Получаем значение курса для валюты Доллар США
    with urlopen(cur) as r:
        usd = etree.parse(r).findtext('.//Valute[@ID="R01235"]/Value')
    # Получаем значение курса для валюты Евро
    with urlopen(cur) as r:
        eur = etree.parse(r).findtext('.//Valute[@ID="R01239"]/Value')
    # Получаем значение котировки для золота
    with urlopen(met) as r:
        au = etree.parse(r).findtext('.//Record[@Code="1"]/Sell')
    # Получаем значение котировки для серебра
    with urlopen(met) as r:
        ag = etree.parse(r).findtext('.//Record[@Code="2"]/Sell')
    # Получаем значение котировки для платины
    with urlopen(met) as r:
        pt = etree.parse(r).findtext('.//Record[@Code="3"]/Sell')
    # Получаем значение котировки для палладия
    with urlopen(met) as r:
        pd = etree.parse(r).findtext('.//Record[@Code="4"]/Sell')
    return render_template('hello.html', **locals())


if __name__ == '__main__':
    app.run()
