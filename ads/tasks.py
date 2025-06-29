from celery import shared_task

@shared_task
def send_ad_report():
    print("Enviando relatório de anúncios...")