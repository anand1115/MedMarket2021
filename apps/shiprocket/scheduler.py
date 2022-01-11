from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, register_job
from django.conf import settings
import requests
import json
from apps.mainadmin.models import ShipRocketToken
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG,timezone=settings.TIME_ZONE)


def update_token():
    print("Token Updated Successfully")
    url = "https://apiv2.shiprocket.in/v1/external/auth/login"
    payload = json.dumps({
                            "email":settings.SHIPROCKET_EMAIL,
                            "password":settings.SHIPROCKET_PASSWORD
                        })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    data=response.json()
    if(response.status_code in [200,202]):
        token=data.get("token")
        if(len(token)>10):
            ShipRocketToken.objects.update_or_create(active=True,defaults={"token":token})
    else:
        print(data)

def start():
    scheduler.add_job(update_token,"interval",minutes=10000,id="promocode_status",max_instances=100000000000,replace_existing=True)
    register_events(scheduler)
    # update_token()
    scheduler.start()