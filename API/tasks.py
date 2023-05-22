from datetime import datetime, timedelta, timezone
import requests
from celery import shared_task
from API.models import Products
from Dewu.settings import PARSE_PERIOD, API_URL


@shared_task()
def parse_spu_ids():
    products = []
    now = datetime.now(timezone.utc)
    for product in Products.objects.all():
        if product.spu_id.strip().isdigit() and now - product.create_time >= timedelta(hours=PARSE_PERIOD):
            products.append(product.spu_id.strip())
    print(products)
    try:
        url = f"{API_URL}parse/"
        requests.post(url, json=products)
    except Exception as e:
        print(e)


@shared_task()
def parse_spu(pk):
    product = Products.objects.get(pk=pk)
    if 'https://dw4.co/t' in product.spu_id:
        r = requests.get(product.spu_id)
        product.spu_id = str(r.url)

    if 'spuId' in product.spu_id:
        product.spu_id = product.spu_id.split('spuId=')[-1].split('&')[0]
        product.save()
        try:
            url = f"{API_URL}parse/"
            requests.post(url, json=[product.spu_id])
        except Exception as e:
            print(e)


@shared_task()
def change_link():
    for product in Products.objects.all():
        if 'https://dw4.co/t' in product.spu_id or 'spuId' in product.spu_id:
            parse_spu.apply_async(args=[product.pk])
