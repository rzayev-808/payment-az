import requests
import json
import binascii
from datetime import datetime
import time
from utils import *
import hashlib
import random
from random import randrange
from hashlib import sha1
import hmac
from binascii import hexlify
import codecs
from invoice import Async

class AzeriCardClass(type):
    def __new__(cls, clsname, bases, attrs, **kwargs):
        newclass= super().__new__(cls, clsname, bases, attrs, **kwargs)

        if newclass.order is not None:
            newclass.register()


        return newclass

class AzeriCard(object, metaclass=AzeriCardClass):

    def __init__(self,*args, **kwargs):
        self.__dict__.update(**kwargs)
        super().__init__()
    
    order = None # order id si mininim 6 reqem olmalidi misal : 100001 : Order id olmadan script run olmur
    
    @classmethod
    def register(cls):
        cls.bank_data(cls)

    def bank_data(self,*args, **kwargs):
        convert = self.__dict__
        irand = random.randint(1, 10000000)
        nonce = substr(hashlib.md5(str(irand).encode('utf-8')).hexdigest(), 0, 16)
        oper_time = gmdate("%Y%m%d%H%I%S")
        TIMESTAMP = oper_time
        NONCE = nonce
        MERCH_GMT = "+4"
        to_sign = str(len(convert['AMOUNT'])) + convert['AMOUNT'] + str(len(convert['CURRENCY'])) + convert['CURRENCY'] + str(
        len(convert['ORDER'])) + convert['ORDER'] + str(len(convert['DESC'])) + convert['DESC'] + str(len(convert['MERCH_NAME'])) + convert['MERCH_NAME'] + str(
        len(convert['MERCH_URL'])) + convert['MERCH_URL'] + str(len(convert['TERMINAL'])) + convert['TERMINAL'] + str(
        len(convert['EMAIL'])) + convert['EMAIL'] + str(len(convert['TRTYPE'])) + convert['TRTYPE'] + str(len(convert['COUNTRY'])) + convert['COUNTRY'] + str(
        len(MERCH_GMT)) + MERCH_GMT +  str(len(oper_time)) + str(oper_time) + str(len(nonce)) + str(nonce) + str(len(convert['BACKREF'])) + convert['BACKREF']
        res = hex2bin(convert['key_for_sign'])
        convert['p_sign'] = hash_hmac('sha1', to_sign, res)
        return self.send_data(**convert)
        


    def send_data(self,*args, **kwargs):
        url = 'https://mpi.3dsecure.az/cgi-bin/cgi_link'
        r = requests.post(url, data=kwargs)
        return r.text

    def callback(self,*args, **kwargs):
        convert = kwargs
        convert['TRTYPE'] = "21",
        irand = random.randint(1, 10000000)
        nonce = substr(hashlib.md5(str(irand).encode('utf-8')).hexdigest(), 0, 16)
        oper_time = gmdate("%Y%m%d%H%I%S")
        t = '21'
        to_sign = str(len(convert['ORDER'])) + convert['ORDER'] + str(len(convert['AMOUNT'])) + convert['AMOUNT'] + str(len(convert['CURRENCY'])) + convert['CURRENCY'] 
        + str(len(convert['RRN'])) + convert['RRN'] + str(len(convert['INT_REF'])) + convert['INT_REF'] + str(len(t)) + str(t) + str(len(convert['TERMINAL'])) 
        + convert['TERMINAL'] + str(len(oper_time)) + str(oper_time) + str(len(nonce)) + str(nonce)
        res = hex2bin(convert['key_for_sign'])
        convert['p_sign'] = hash_hmac('sha1', to_sign, res)
        print(convert)
        return self.send_data(**kwargs)


    def data_result(self, *args, **kwargs):
        kwargs['send_email'] = False
        if kwargs['ACTION'] == '0':
            check = self.callback(**kwargs)
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
            if check == '0':
                return {'status':'Ugurlu əməliyyat', 'action':kwargs['ACTION']}
            if check == '1':
                return 'Duplicate transaction detected;'
            if check == '2':
                return 'Transaction declined;'
            if check == '3':
                return 'Transaction processing fault.'
        elif kwargs['ACTION'] == 'RC':
            return 'Error' + "" + kwargs['ACTION']


    def reversal(self,*args, **kwargs):
        convert = kwargs
        convert['TRTYPE'] = '22'
        irand = random.randint(1, 10000000)
        nonce = substr(hashlib.md5(str(irand).encode('utf-8')).hexdigest(), 0, 16)
        oper_time = gmdate("%Y%m%d%H%I%S")
        to_sign =  str(len(convert['AMOUNT'])) + convert['AMOUNT'] + str(len(convert['CURRENCY'])) + convert['CURRENCY'] + str(len(convert['RRN'])) + convert['RRN'] + str(len(convert['INT_REF'])) + convert['INT_REF'] + str(len(convert['TRTYPE'])) + convert['TRTYPE'] + str(len(convert['TERMINAL'])) + convert['TERMINAL'] + str(len(oper_time)) + str(oper_time) + str(len(nonce)) + str(nonce)
        res = hex2bin(convert['key_for_sign'])
        convert['p_sign'] = hash_hmac('sha1', to_sign, res)
        check = self.send_data(**kwargs)
        if check == '0':
            return {'status':'Ugurlu əməliyyat', 'action':kwargs['ACTION']}
        if check == '1':
            return 'Duplicate transaction detected;'
        if check == '2':
            return 'Transaction declined;'
        if check == '3':
            return 'Transaction processing fault.'

        
