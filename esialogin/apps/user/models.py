from django.db import models
from django.shortcuts import redirect
from hashlib import md5
import random
import string
from esialogin.settings import SYSTEMNAME, SHORTSYSTEMNAME
import logging

log = logging.getLogger('request')



def getUserInformation(data):
    userInformation = User.objects.filter(snils = data['snils'])[:1]
    if len(userInformation) > 0:
        userInformation = userInformation[0]
    else:
        userInformation = User()
        userInformation.snils = data['snils']
        userInformation.save()
    return userInformation

def checkRights(func):
    def _get_obj_type(request, obj_type="", obj_adds="", *args, **kwargs):
        loginInformation = UserLogin.isAuthCorrect(request.session)
        if loginInformation['error']:
            return redirect('login:index')
        
        userInformation = getUserInformation(loginInformation)
        adds = {
            'sysname': SYSTEMNAME,
            'shortsysname': SHORTSYSTEMNAME
        }
        return func(request, obj_id=userInformation, obj_adds=adds, *args, **kwargs)
    return _get_obj_type



class User(models.Model):
    
    id = models.BigAutoField(primary_key = True)
    datecreated = models.DateTimeField('Дата создания', auto_now_add = True)
    datechanged = models.DateTimeField('Дата изменения', auto_now = True)
    snils = models.CharField('SNILS', max_length=20, default='')
    fullname = models.CharField('ФИО', max_length=200, default='user')
    email = models.CharField('Эл. почта', max_length=40, default='')
    phone = models.CharField('Телефон', max_length=20, default='')


    def __str__(self):
        return '{id} {fullname}'.format(id = self.id, fullname = self.fullname)

    class Meta:
        verbose_name = 'Информация о пользователе'
        verbose_name_plural = 'Информация о пользователях'



class UserLogin(models.Model):

    id = models.BigAutoField(primary_key = True)
    datecreated = models.DateTimeField('Дата создания', auto_now_add = True)
    datechanged = models.DateTimeField('Дата изменения', auto_now = True)
    login = models.CharField('LOGIN', max_length=20)
    snils = models.CharField('SNILS', max_length=20, default='0')
    password_hash = models.CharField('Хэш пароля', max_length=40)
    session_hash = models.CharField('Хэш сессии', max_length=40)
    enabled = models.BooleanField('Активен?', default=True)


    def generateRandomHash(self, hashLength = 11):
        letters = string.ascii_lowercase
        md5sum = ''.join(random.sample(letters, hashLength))
        return md5(md5sum.encode('utf-8')).hexdigest()

    def getPasswordHash(self, inputPass):
        salt = '543'
        password = '%s%s' % (inputPass, salt)
        md5sum = md5(password.encode('utf-8')).hexdigest()
        md5sum = md5(md5sum.encode('utf-8')).hexdigest()
        return md5sum

    def checkPassword(self, inputPass):
        if len(inputPass) < 3:
            return False
        return self.password_hash == self.getPasswordHash(inputPass)

    def isAuthCorrect(session):
        d = {'login': '', 'snils': '', 'error': True}
        if (session.has_key('username') and (session.has_key('sessionhash'))):
            username = session['username']
            sessionhash = session['sessionhash']
            loginInfo = UserLogin.objects.filter(login = username, session_hash = sessionhash)[:1]
            if len(loginInfo) > 0:
                d = {
                    'login': loginInfo[0].login, 
                    'snils': loginInfo[0].snils,
                    'error': False
                }
                return d
        return d


    def __str__(self):
        return '{id} {login}'.format(id = self.id, login = self.login)

    class Meta:
        verbose_name = 'Логин пользователя'
        verbose_name_plural = 'Логин пользователей'
