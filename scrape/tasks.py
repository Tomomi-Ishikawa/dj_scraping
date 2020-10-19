import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from .models import Request
from .views import Request
from celery import shared_task

def get_yahooauction(url):
    res = requests.get(url)
    soup = bs(res.content, 'html.parser')
    items = soup.findAll(class_='Product')
    return [
        {
            'title': item.find(class_='Product__titleLink').text.strip(),
            'url': item.find(class_='Product__titleLink').get('href'),
            'picture': item.find('img').get('src')
        }
        for item in items 
    ]


@shared_task #python デコレータ
def start_task(_uuid):
    gcs_bucket = 'gs://scr_django'
    obj = Request.objects.get(uuid=_uuid)
    # スクレイピング
    result = get_yahooauction(obj.url)
    df = pd.DataFrame(result)
    # file名を定義
    filename = f'{gcs_bucket}/{_uuid}.pkl'
    # save data
    df.to_pickle(filename)
    return True