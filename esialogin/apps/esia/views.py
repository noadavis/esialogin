from django.shortcuts import render, redirect
from django.utils.http import urlencode
from django.http import HttpResponse
from crypto.models import Crypto
from base64 import b64encode, urlsafe_b64decode
from urllib import request as urllibRequest, parse as urllibParse
from esialogin.settings import SYSTEM_URL, ESIA_SCOPE, ESIA_CLIENT_ID, ESIA_TEST, SYSTEMNAME
from datetime import datetime
from pytz import timezone
import uuid
import json

import logging

log = logging.getLogger('service')
crypro = Crypto(debug = True)

if ESIA_TEST:
    authorization_base_url = 'https://esia-portal1.test.gosuslugi.ru/aas/oauth2/ac'
    token_url = 'https://esia-portal1.test.gosuslugi.ru/aas/oauth2/te'
    info_url = 'https://esia-portal1.test.gosuslugi.ru/rs/prns/'
else:
    authorization_base_url = 'https://esia.gosuslugi.ru/aas/oauth2/ac'
    token_url = 'https://esia.gosuslugi.ru/aas/oauth2/te'
    info_url = 'https://esia.gosuslugi.ru/rs/prns/'
redirect_url = '%s/%s' % (SYSTEM_URL, 'esia/esia/')



def index(request):
    removeSession(request.session)

    secret = generateSecret()
    if secret is not None:
        authorization_url = urlencode({
            'client_id': ESIA_CLIENT_ID,
            'scope': ESIA_SCOPE,
            'state': secret['state'],
            'timestamp': secret['timestamp'],
            'client_secret': secret['client_secret'],
            'response_type': 'code',
            'access_type': 'online',
            'redirect_uri': redirect_url
        })
        
        authorization_url = '%s?%s' % (authorization_base_url, authorization_url) 
        request.session['oauth_state'] = secret['state']
        
        #Редирект для авторизации пользователя в есиа и получения кода авторизации
        #Сохраняем oauth_state в сессии для проверки подлинности ответа
        return redirect(authorization_url)
    else:
        return render(request, 'login.html', {'sysname': SYSTEMNAME, 'error': 'esia error'})



def callback(request):

    if 'error' in request.GET:
        log.error('esia error: %s' % request.GET['error'])
        if 'error_description' in request.GET:
            log.error('esia error_description: %s' % request.GET['error_description'])
        return render(request, 'login.html', {'sysname': SYSTEMNAME, 'error': 'esia error'})

    if request.session.has_key('oauth_state'):
        if 'code' in request.GET and 'state' in request.GET:
            code = request.GET['code']

            #Проверяем подлинность пришедшего запроса
            if request.session['oauth_state'] == request.GET['state']:
                
                secret = generateSecret()
                if secret is not None:
                    
                    
                    
                    oauthTokenParams = {
                        'client_id': ESIA_CLIENT_ID,
                        'scope': ESIA_SCOPE,
                        'state': secret['state'],
                        'timestamp': secret['timestamp'],
                        'client_secret': secret['client_secret'],
                        'grant_type': 'authorization_code',
                        'code': code,
                        'token_type': 'Bearer',
                        'access_type': 'online',
                        'redirect_uri': redirect_url
                    }
                    
                    #По полученному коду авторизации отправляем запрос на получение токена
                    answer = getPostAnswer(url = token_url, data = oauthTokenParams, headerType = None)
                
                    if answer is None:

                        log.error('callback: token post answer is None')

                    else:

                        if 'state' in answer and 'access_token' in answer:
                            
                            #Проверяем подлинность пришедшего ответа
                            if secret['state'] == answer['state']:
                                
                                access_token = answer['access_token']
                                #Из пришедшего ответа получаем идентификатор пользователя есиа
                                oauth_sbj_id = getEsiaUserId(access_token)
                                
                                if oauth_sbj_id is not None:
                                    #log.info('callback: access_token: %s' % access_token)
                                    #log.info('callback: oauth_sbj_id: %s' % oauth_sbj_id)
                                    
                                    request.session['oauth_token'] = access_token
                                    request.session['oauth_sbj_id'] = oauth_sbj_id

                                    return redirect('login:esia')
                                        
                            else:
                                log.error('callback: esia return wrong state value')
                        else:
                            log.error('callback: state or access_token not found in answer')
                        


                else:
                    #Ошибка подписания
                    log.error('callback: sign error')

            else:
                #Созданный на первом шаге state не совпадает с пришедшим в запросе
                log.error('callback: esia return wrong state value')
        else:
            #Не корректный get запрос, возможно ктото пытается зайти на урл вручную
            log.error('callback: code or state not found in request.GET')
    else:
        #Первый шаг не пройден, возможно ктото пытается зайти на урл вручную
        log.error('callback: oauth_state not found')

    return render(request, 'login.html', {'sysname': SYSTEMNAME, 'error': 'esia error'})







def removeSession(reqSession):
    try:
        if reqSession.has_key('username') :
            del reqSession['username']
        if reqSession.has_key('sessionhash'):
            del reqSession['sessionhash']
        if reqSession.has_key('oauth_state') :
            del reqSession['oauth_state']
        if reqSession.has_key('oauth_token'):
            del reqSession['oauth_token']
        if reqSession.has_key('oauth_sbj_id'):
            del reqSession['oauth_sbj_id']
    except Exception as ex:
        log.error('removeSession Exception: {ex}'.format(ex = ex))

def generateSecret():
    state = str(uuid.uuid1())
    timestamp = datetime.now(timezone('Europe/Moscow')).strftime("%Y.%m.%d %H:%M:%S %z")
    client_secret_str = '%s%s%s%s' % (
        ESIA_SCOPE,
        timestamp,
        ESIA_CLIENT_ID,
        state
    )
    client_secret = crypro.signEsiaString(client_secret_str)
    if client_secret is not None:
        if not client_secret['error']:
            return {
                'state': state,
                'timestamp': timestamp,
                'client_secret': client_secret['signature']
            }
    return None

def getEsiaUserId(token):
    try:
        token_parts = token.split('.')
        if len(token_parts) < 3:
            return None
        #Исправляем возможный incorrect padding
        part = token_parts[1] + "==="
        partJson = urlsafe_b64decode(part.encode("utf-8")).decode("utf-8")
        partJson = json.loads(partJson)
        if 'urn:esia:sbj_id' in partJson:
            return partJson['urn:esia:sbj_id']
    except Exception as ex:
        log.error('getEsiaUserId: exception while get esiaId: %s' % ex)
    return None

def getPostAnswer(url, data, headerType = None):
    jsonResponse = None
    try:
        if headerType == 'json':
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            encodedData = json.dumps(data).encode('UTF-8')
        elif headerType == 'authorization':
            headers = {
                "Authorization": "Bearer %s" % data
            }
            url = '%s%s' % (info_url, url)
        else:
            headers = {}
            encodedData = urllibParse.urlencode(data).encode()

        if headerType == 'authorization':
            postRequest = urllibRequest.Request(url, headers = headers)
        else:
            postRequest = urllibRequest.Request(url, data = encodedData, headers = headers)
        
        postResponse = urllibRequest.urlopen(postRequest)
        postContent = postResponse.read().decode('UTF-8')
        jsonResponse = json.loads(postContent)
    except Exception as ex:
        log.error('getPostAnswer: post request exception: %s' % ex)
    return jsonResponse
