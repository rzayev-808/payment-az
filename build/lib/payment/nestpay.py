import requests
import datetime 
import hashlib
import base64
import time
from utils import *
from invoice import Async


class NestPay():

    def __init__(self,**kwargs):
        self.__dict__.update(**kwargs)
        super().__init__()

    def bank_data(self, *args, **kwargs):
        convert = self.__dict__
        string = convert['clientId'] + convert['oid'] + convert['amount'] + convert['okUrl'] + convert['failUrl'] + convert['islemtipi'] + convert['instalment'] + str(convert['rnd']) + convert['storekey']
        string_to_hash = convert_string_to_hash(string).decode()
        convert['hash']= string_to_hash
        return self.data_send(**convert)

    def data_send(self, *args, **kwargs):
        url = '{0}'.format(kwargs['post_url'])
        del kwargs['post_url']
        post = requests.post(url, data=kwargs)
        return post.content


    def data_result(self,**kwargs):

        storekey = kwargs['storekey']
        hashparams = kwargs['HASHPARAMS']
        hashparamsval = kwargs['HASHPARAMSVAL']
        hashparam = kwargs['HASH']
        paramsval = ''
        index1 = 0
        index2 = 0
        while index1< len(hashparams):
            index2 = hashparams.find(':', index1)
            s = substr(hashparams,index1,index2-index1)
            vl = kwargs.get(f'{s}')
            paramsval = paramsval + vl
            index1 = index2 + 1
        hashval = paramsval + storekey
        hashcon = convert_string_to_hash(hashval).decode()
        if hashparams != None:
            if paramsval != hashparamsval or hashparam != hashcon:
                return 'Security warning. Hash values mismatch'
            else:
                mdStatus = kwargs['mdStatus']
                if mdStatus == "1" or mdStatus == "2" or mdStatus == "3" or mdStatus == "4":
                    kwargs['send_email'] = False
                    if kwargs['send_email'] == True:
                        send_mail=Async()
                        send_mail.function(
                            port=kwargs.get('port'),
                            hostname=kwargs.get('hostname'),
                            password=kwargs.get('password'),
                            sender = kwargs.get('sender'),
                            to = kwargs.get('to'),
                            content = kwargs.get('content'),
                        )
                    return '3D Authentication is successful.'
                else:
                    return '3D authentication unsuccesful.'
        else:
            return 'Hash values error. Please check parameters posted to 3D secure page.'
        
        


