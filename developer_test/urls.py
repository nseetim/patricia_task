from django.urls import path
from developer_test.api.views import webhook_handler

app_name = 'developer_test'

urlpatterns = [
    path('<username>/', webhook_handler, name='webhook_handler'),
]