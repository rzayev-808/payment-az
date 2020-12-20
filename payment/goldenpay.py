import hashlib
import requests
import xml.etree.ElementTree as ET


class GoldenPay():
    def __init__(self, *args, **kwargs):
        self.__dict__.update(**kwargs)
        super().__init__()


    def bank_data(self, *args, **kwargs):
        data = self.__dict__
        amount = data['amount'] * 100
        merchantName = data['merchantName']
        authKey = data['authKey']
        cardType = data['cardType']
        description = data['description']
        con = authKey + merchantName + cardType + str(amount) + description
        hashCode = hashlib.md5(con.encode("utf-8")).hexdigest()
        h  = {
            "merchantName": merchantName,
            "cardType": cardType,
            "hashCode": hashCode,
            "lang": "lv",
            "amount":amount,
            "description":description

        }
        return self.getPaymentKey(**h)

    def getPaymentKey(self, *args, **kwargs):
        send = kwargs
        print(send)
        url = "https://rest.goldenpay.az/web/service/merchant/getPaymentKey"
        l = requests.post(url, json=send)
        root = ET.fromstring(l.content)
        for x in root.iter('paymentKey'):
            
            return {'url':"https://rest.goldenpay.az/web/pay/" + x.text, 'paymentKey':x.text}


    def getPaymentResult(self,*args, **kwargs):
        data = kwargs
        key =  data['authKey'] + data['paymentKey']
        w = hashlib.md5(key.encode("utf-8")).hexdigest()
        url = "https://rest.goldenpay.az/web/service/merchant/getPaymentResult?payment_key={}&hash_code={}".format(data['paymentKey'],w)
        post = requests.post(url)
        return post


