import requests
import json

from django.contrib.sites.shortcuts import get_current_site
import rest_framework
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.authtoken.models import Token

from developer_test.models import AppUser,Transaction


@api_view(['POST', ])
@permission_classes(())
def registration(request):
    current_site = get_current_site(request)
    user = request.user
    name = request.data.get('name')
    username = request.data.get('username')
    
    if not name and username:
        return Response({
            'message': 'One of the required fields are missing'
        }, status=status.HTTP_417_EXPECTATION_FAILED)

    new_user = AppUser.objects.create(name=name, username=username)
    try:
        new_user_api_key = Token.objects.get(user=new_user)
    except Token.DoesNotExist:
        new_user_api_key = Token.objects.create(user=new_user)
    new_user.api_key = new_user_api_key.key
    new_user.web_hook_url = "http://"+str(current_site)+"/webhook/"+new_user.username+"/"
    new_user.save()
    return Response({
        'message': f'Congratulation {new_user}, your registeration was successful',
        'info': 'Keep your api_key safe and secure it would be required to authenticate every api call you make',
        'API_KEY': new_user.api_key,
        'web_hook_url': new_user.web_hook_url,
    }, status=status.HTTP_200_OK)


@api_view(['POST', ])
def trnx_registration(request):
    """
    Transaction registeration view which sends a payload to the users webhook url after writing the 
    transaction to the DB and returns a status code of 200 on successfully doing so or a status 400 alongside
    a mesage informing the user on the inability to completely process the request.

    A username and api_key is sent in the post request, the api_key is then used to authenticate the user
    alog side the username sent to ensure the api_key wasnt just gotten and used by another fellow, usernames
    for this reason are also case sensitive

    """
    unprovided_fields = []
    required_fields = {
        'api_key': request.data.get('api_key'),
        'username': request.data.get('username'),
        'price': request.data.get('price'),
        'transaction_reference': request.data.get('transaction_reference'),
        'client_id': request.data.get('client_id'),
        'status': request.data.get('status'),
    }
    
    for key_, value_, in required_fields.items():
        if not value_:
            unprovided_fields.append(key_)
    if unprovided_fields:
        return Response({
            'message': f'The {unprovided_fields} field(s) are missing and are required'
        }, status=status.HTTP_417_EXPECTATION_FAILED)
    try:
        verified_user = AppUser.objects.get(username=required_fields['username']\
            , api_key=required_fields['api_key'])
    except AppUser.DoesNotExist:
        verified_user = None
    if verified_user:
        new_transaction = Transaction.objects.create(user=verified_user,transaction_reference=required_fields['transaction_reference']\
            , price=required_fields['price'], client_id=required_fields['client_id']\
                , status=required_fields['status'])
        data = {
            'transaction_reference':new_transaction.transaction_reference,
            'price': new_transaction.price,
            'client_id': new_transaction.client_id,
            'status': 'successful',
        }
        headers = {
            'Content-Type': 'application/json',
            'Cach-Control': 'no-cache',
        }
        json_dump = json.dumps(data)
        response = requests.post(verified_user.web_hook_url, data=json_dump, headers=headers)
        print(response.json(),f'status code: {response.status_code}')
        return Response({
            'message': f'Congratulation {verified_user}, your transaction was successfully registered',
            'transaction_reference': f'Transaction Reference {new_transaction.transaction_reference}',
            'price': new_transaction.price,
            'client_id': new_transaction.client_id,
        }, status=status.HTTP_200_OK)
    return Response({
            'message': 'Sorry there is an issue with this request check the username or api_key again'
        }, status=status.HTTP_400_BAD_REQUEST)

# The webhook handler view recieves the webhook and returns a status 200
@api_view(['POST', ])
def webhook_handler(request, username):
    payload = request.data
    print(payload)
    return Response({
        'message': "webhook recieved by user's url"
    }, status=status.HTTP_200_OK)
    