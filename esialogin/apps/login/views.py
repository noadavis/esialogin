from django.shortcuts import render, redirect
from user.models import UserLogin, User
from esialogin.settings import SYSTEMNAME
import logging

log = logging.getLogger('request')



def getPasswordLogin(username, password):
    loginInfo = UserLogin.objects.filter(login = username)[:1]
    loginIsCorrect = False
    sessionHash = ''
    error = ''

    if len(loginInfo) > 0:
        loginInfo = loginInfo[0]
        if not loginInfo.enabled:
            loginIsCorrect = False
            error = 'user disabled'
        else:
            loginIsCorrect = loginInfo.checkPassword(password)
            if not loginIsCorrect:
                error = 'bad user password'
    else:
        loginIsCorrect = False
        error = 'user not exist'
        
    if loginIsCorrect:
        sessionHash = loginInfo.generateRandomHash()
        loginInfo.session_hash = sessionHash
        loginInfo.save()

    return {
        'loginIsCorrect': loginIsCorrect,
        'sessionHash': sessionHash,
        'username': username,
        'error': error
    }



def index(request):
    
    if not UserLogin.isAuthCorrect(request.session)['error']:
        return redirect('about:index')
    else:
        removeSession(request.session)
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        result = getPasswordLogin(username, password)
        
        if result['loginIsCorrect']:
            request.session['username'] = result['username']
            request.session['sessionhash'] = result['sessionHash']
            return redirect('about:index')
        else:
            return render(request, 'login.html', {'sysname': SYSTEMNAME, 'error': result['error']})

    return render(request, 'login.html', {'sysname': SYSTEMNAME, 'error': ''})



def esia(request):
    userInfo = None
    
    if request.session.has_key('oauth_token') and request.session.has_key('oauth_sbj_id'):
        from esia.views import getPostAnswer
        
        oauth_token = request.session['oauth_token']
        oauth_sbj_id = request.session['oauth_sbj_id']
        
        #Отправляем запрос на получение данных из есиа
        userInfo = getPostAnswer(url = oauth_sbj_id, data = oauth_token, headerType = 'authorization')

    else:
        log.error('oauth_token or oauth_sbj_id not found')
        return render(request, 'login.html', {'sysname': SYSTEMNAME, 'error': 'esia error'})


    if userInfo is not None:
        if 'snils' in userInfo:
            userInfo['snils'] = userInfo['snils'].replace(' ', '').replace('-', '').strip()
        else:
            userInfo = None

    if userInfo is not None:
        result = getEsiaLogin(userInfo)
        if result['loginIsCorrect']:
            request.session['username'] = result['username']
            request.session['sessionhash'] = result['sessionHash']
            removeEsiaSession(request.session)
            return redirect('about:index')
        else:
            return render(request, 'login.html', {'sysname': SYSTEMNAME, 'error': result['error']})

    return render(request, 'login.html', {'sysname': SYSTEMNAME, 'error': ''})


def getEsiaLogin(data):
    loginIsCorrect = False
    sessionHash = ''
    error = ''

    if 'snils' in data:
        #username, password для поддержки логина по паролю
        username = data['snils']
        password = data['snils']
        
        loginIsCorrect = True
        loginInfo = UserLogin.objects.filter(snils = data['snils'])[:1]
        try:
            if len(loginInfo) > 0:
                #Если пользователь существует проверяем статус блокировки
                loginInfo = loginInfo[0]
                if not loginInfo.enabled:
                    loginIsCorrect = False
                    error = 'user disabled'

            else:
                #Если пользователя не существует создаем записи в базе
                loginInfo = UserLogin()
                loginInfo.login = username
                loginInfo.snils = data['snils']
                loginInfo.password_hash = loginInfo.getPasswordHash(password)
                loginInfo.session_hash = ''
                loginInfo.enabled = True

                userInfo = User.objects.filter(snils = data['snils'])[:1]
                if len(userInfo) > 0:
                    userInfo = userInfo[0]
                else:
                    userInfo = User()
                userInfo.fullname = ('%s %s %s' % (data['lastName'], data['firstName'], data['middleName'])).strip()
                userInfo.snils = data['snils']
                userInfo.phone = ''
                userInfo.email = ''
                userInfo.save()

                log.info('user created: login: %s, password: %s' % (loginInfo.login, password))

            sessionHash = loginInfo.generateRandomHash()
            loginInfo.session_hash = sessionHash
            loginInfo.save()
        except Exception as ex:
            loginIsCorrect = False
            error = 'runtime error'
            log.error('getEsiaLogin: %s' % ex)
    else:
        error = 'bad esia answer'
        log.error('getEsiaLogin: %s' % error)
        log.error(data)
    return {
        'loginIsCorrect': loginIsCorrect,
        'sessionHash': sessionHash,
        'username': username,
        'error': error
    }



def removeSession(reqSession):
    try:
        if reqSession.has_key('username') :
            del reqSession['username']
        if reqSession.has_key('sessionhash'):
            del reqSession['sessionhash']
    except Exception as ex:
        log.error('removeSession: %s' % ex)


def removeEsiaSession(reqSession):
    try:
        if reqSession.has_key('oauth_state'):
            del reqSession['oauth_state']
        if reqSession.has_key('oauth_token'):
            del reqSession['oauth_token']
        if reqSession.has_key('oauth_sbj_id'):
            del reqSession['oauth_sbj_id']
    except Exception as ex:
        log.error('removeEsiaSession: %s' % ex)


def logout(request):
    removeSession(request.session)
    removeEsiaSession(request.session)
    return redirect('login:index')
