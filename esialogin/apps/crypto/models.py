from esialogin.settings import BASE_DIR, SIGN_TMP_PATH, SIGN_PASSWORD, SHA1_PUBLIC_KEY
from uuid import uuid4
from os.path import exists
from os import makedirs
from shutil import rmtree
from base64 import b64decode, urlsafe_b64encode
from subprocess import Popen, PIPE
import logging

log = logging.getLogger('service')

class Crypto(object):
    error = False
    errorDescription = ''
    debug = False

    def __init__(self, debug = False):
        self.debug = debug


    def setError(self, description = ''):
        self.error = True
        self.errorDescription = description


    def signPrepare(self):
        self.error = False
        self.errorDescription = ''

        THREAD_ID = uuid4().hex
        prepareSets = {
            'thread_id': THREAD_ID,
            'sign_cmd': '/opt/cprocsp/bin/amd64/cryptcp -signf -dir "%(dir)s" -strict -cert -detached -thumbprint %(sha1)s -pin %(password)s "%(msg_file)s"',
            'msg_file': '%s%s/msg' % (SIGN_TMP_PATH, THREAD_ID),
            'sign_path': '%s%s' % (SIGN_TMP_PATH, THREAD_ID)
        }
        
        if not exists(prepareSets['sign_path']):
            try:
                makedirs(prepareSets['sign_path'])
            except Exception as ex:
                self.setError('exception while create path: %s' % ex)
        
        if self.debug:
            log.info(prepareSets)

        return prepareSets



    def signEsiaString(self, esiaString, urlSafe = True):
        prepareSets = self.signPrepare()
        signature_value = ''
        
        try:
            #write string to file
            f = open(prepareSets['msg_file'], "w+")
            f.write(esiaString)
            f.close()
        except Exception as ex:
            self.setError('cant write esiaString to file: %s' % ex)
        
        if not self.error:
            #sign file with /opt/cprocsp/bin/amd64/cryptcp
            proc = Popen(
                prepareSets['sign_cmd'] % {
                    'dir': prepareSets['sign_path'], 
                    'sha1': SHA1_PUBLIC_KEY, 
                    'password': SIGN_PASSWORD, 
                    'msg_file': prepareSets['msg_file']
                },
                shell=True,
                stdout=PIPE, stderr=PIPE
            )
            proc.wait()
            proc.communicate()

            try:
                #read signed data from /opt/cprocsp/bin/amd64/cryptcp
                f = open(prepareSets['msg_file'] + '.sgn', "rb")
                signature_bytes = f.read()
                f.close()
            except Exception as ex:
                self.setError('cant read signature from file: %s' % ex)
        
        if not self.error:
            signature_value = signature_bytes.decode('UTF-8').replace('\n', '')
            
            if urlSafe:
                signature_bytes = b64decode(signature_value)
                signature_value = urlsafe_b64encode(signature_bytes).decode('UTF-8')
        
        #delete tmp files
        if not self.debug:
            try:
                if exists(prepareSets['sign_path']):
                    rmtree(prepareSets['sign_path'])
            except:
                log.error('cant delete tmp directory')
        
        res = {
            'signature': signature_value,
            'error': self.error,
            'description': self.errorDescription
        }

        return res
