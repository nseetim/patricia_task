from django.urls import path
from .views import registration, trnx_registration

app_name = 'developer_test'


urlpatterns = [
    # Registeration url for registering the new users
    path('register/', registration, name='registration'), 
    # Transaction registeration url, for recording transaactions
    path('trnx_registration/', trnx_registration, name='transaction_registration'),
]