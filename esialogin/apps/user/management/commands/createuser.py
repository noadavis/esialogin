from django.core.management.base import BaseCommand, CommandError
from user.models import User, UserLogin
import logging

log = logging.getLogger('service')



class Command(BaseCommand):
    help = 'Create user'

    def add_arguments(self, parser):
        parser.add_argument('--login', action='append', type=str)
        parser.add_argument('--password', action='append', type=str)

    def handle(self, *args, **options):
        
        login = ''
        if options['login'] is not None:
            login = options['login'][0]
        password = ''
        if options['password'] is not None:
            password = options['password'][0]

        if (len(login) > 2) and (len(password) > 2):

            newUser = True
            userLogin = UserLogin.objects.filter(login = login)[:1]
            newUser = len(userLogin) == 0

            try:
                if newUser:
                    user = User()
                    user.snils = '111-111-111-11'
                    user.fullname = login
                    user.email = '%s@local.loc' % login
                    user.phone = '9101234567'
                    user.save()

                    userLogin = UserLogin()
                    userLogin.login = login
                    userLogin.snils = '111-111-111-11'
                    userLogin.session_hash = '1'
                else:
                    userLogin = userLogin[0]

                userLogin.password_hash = userLogin.getPasswordHash(password)
                userLogin.save()
                
                if newUser:
                    log.info('user: %s created' % login)
                else:
                    log.info('password for user: %s changed' % login)

            except Exception as ex:
                log.error('exception while create user: %s' % ex)

        else:
            log.error('login or password not set')
