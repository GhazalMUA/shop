from celery import Celery
from datetime import timedelta
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE' , 'A.settings')    #Here you can see the location of your project. For example, A.settings is the settings for your current project
celery_app= Celery('A')    #the name you assign to your Celery app must match your project name.

celery_app.autodiscover_tasks()   #this method is finding your apps where it can find task.py , it execute this file

celery_app.conf.broker_url= 'amqp://rabbitmq'   #first you should check this command 'brew services start rabbitmq' and then check this command to check the status of rabbitmq 'brew services list'
celery_app.conf.result_backend= 'rpc://'
celery_app.conf.task_serializer= 'json'
celery_app.conf.result_serializer= 'pickle'
celery_app.conf.accept_content= ['json' , 'pickle']
celery_app.conf.result_expires= timedelta(days=1)
celery_app.conf.task_always_eager= False   #means should i make a wait for a client to complete my task?
celery_app.conf.worker_prefetch_multiplier = 4    #the maximum capacity that one worker can do a task. if your tasks are simple you can set it to the 4 but if your tasks are heavyyou can set it to 1
