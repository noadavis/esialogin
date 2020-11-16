from django.core.management.base import BaseCommand, CommandError
from crypto.models import Crypto
import logging

log = logging.getLogger('service')



class Command(BaseCommand):
    help = 'Sign test'
    
    def add_arguments(self, parser):
        parser.add_argument('--sign', action='append', type=str)

    def handle(self, *args, **options):
        
        sign = ''
        if options['sign'] is not None:
            sign = options['sign'][0]
        
        if len(sign) > 2:
            log.info('string to sign: "%s"' % sign)
            crypto = Crypto(True)
            log.info(crypto.signEsiaString(sign))
