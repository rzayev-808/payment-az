# odeme sistemleri ucun modul

Hazirda Azericard , NestPay, GoldenPay destekleyir

Modulda async odeme neticesini gonderen function var . Callback a gelen data ya gore 'success' emaili gonderir .

default olarag False di

aktiv etmek ucun :

callbackda data_result a gonderdiyimiz request.POST da send_email = True ve:

```python
send_email = True
sender = ''
to = ''
content = ''
hostname='',
port='',
username='',
password='',

```
gondermeyiniz bes edir

```python
# Azericard ucun example 


@csrf_exempt
def callback(request):
    ........
    if request.method == 'POST':
        
        data = request.POST
        # email gondermek isdediyiniz teqdirde
        ###################
        data['send_email'] = True
        data['sender'] = '' # gonderen
        data['to'] = '' # kime
        data['content'] = '' # mail terkibi ```html``` qebul edir
        data['hostname']='', # email server
        data['port']= 465, # port integer olmalidi
        data['username']='', # email login
        data['password']='', # email password
        ####################### eger email gondermek isdemirsinizse commente aldigim hisseni gondermeye ehtiyac yoxdur
        result = AzeriCard.data_result(**data)
        return HttpResponse(result)
    else:
        return HttpResponse("Not found")


```

# Example NestPay

```python



from payment.nestpay import NestPay
from payment.utils import microtime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt




def payment(request):
    ......
    temp = NestPay(
        clientId = '', # bank terefinden verilir
        amount = '', # mebleg : 1.00 azn (float)
        oid = '', # order id unique - di
        okUrl = '', # callback url. Success den sonra bura post gonderilir
        failUrl = '', # error url 
        rnd = microtime(),
        storekey = '2', # bank terefinden verilir
        storetype = '', # bank terefinden verilir
        lang = 'en', # hansi dilde odeme sehvesine redirect edecek
        islemtipi = 'Auth', # default 
        hash = '', # hash edirik default bosh stringdi
        refreshtime = '5', # sehifeler arasinda redirect timeout
        instalment='', # taksid
        currency = '944', # Azerbaycan manatinin kodu
        post_url = 'https://entegrasyon.asseco-see.com.tr/fim/est3Dgate' # odeme sehifesi
        ).bank_data()
   
    return HttpResponse(temp)

# callback yuxarda paymentde qeyd edeceyimiz okUrl di ve o url e bank post gonderir
@csrf_exempt
def callback(request):
    ........
    if request.method == 'POST':
        data = request.POST
        data['storekey'] = '' #bank terefinden verilir
        result = NestPay.data_result(**data)
        return HttpResponse(result)
    else:
        return HttpResponse("Not found")


```


# Example Azericard




```python




from payment.azericard import AzeriCard
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt




def payment(request):
    ......
    temp = AzeriCard(
        AMOUNT = '1',
        CURRENCY = "AZN",
        ORDER = '100001', # order id si mininim 6 reqem olmalidi misal : 100001 : Order id olmadan script run olmur
        TERMINAL = "", # bank terefinden verilir
        TRTYPE = "1", # Auth
        key_for_sign = "", #bank terefden onceden verilir
        DESC = "",# description
        MERCH_NAME = "", #magaza adi
        MERCH_URL = "", # callback sehifesi
        EMAIL = "", # emailiniz
        COUNTRY = "AZ", 
        BACKREF = "",# geri donus sehifesi
        ).bank_data()
    
    return HttpResponse(temp)

# callback yuxarda paymentde qeyd edeceyimiz MERCH_URL di ve o url e bank post gonderir
@csrf_exempt
def callback(request):
    ........
    if request.method == 'POST':
        data = request.POST
        data['key_for_sign'] = '' # bank terefden onceden verilir
        result = AzeriCard.data_result(**data)
        # eger odenisin reversal nezerde tutmusunuzsa data['RRN'] ve data['INT_REF'] ni order.models de save edin
        # Example
        if result['action'] == '0':
        try:
            order = Order.models.get(id=data['ORDER'])
            order.rrn == data['RRN']
            order.int_ref = data['INT_REF']
        except:
            pass
        return HttpResponse(result)
    else:
        return HttpResponse("Not found")

# ordenisin geri qaytarilmasi lazim oldugu halda (reversal)
def payment_reversal(request):
    data = {}
    data['key_for_sign'] = '' # bank terefden onceden verilir
    data['AMOUNT'] = '1';
	data['CURRENCY'] = 'AZN';
	data['ORDER'] = '000001';
	data['RRN'] = '';			#Bank reference number
	data['INT_REF'] = '';		# Internal reference number
	data['TERMINAL'] = '77777777';			
    reversal = AzeriCard.reversal(**data)
    return HttpResponse(result) 



```


# Example GoldenPay




```python

from payment.goldenpay import GoldenPay
from django.http import HttpResponseRedirect



def payment(request):
    temp = GoldenPay(
        amount = 1, # qiymet
        merchantName = "", # goldenpay terefden verilir 
        authKey = "", # goldenpay terefden verilir 
        cardType = "", # (Visa=v, Mastercard=m)
        description = "", # 
        ).bank_data()
    ######## Eger odenisin neticesini oyrenmek isdeyirsinizse remp['paymentKey'] database save edin 
    # Example    Order.objects.create(key = remp['paymentKey'])

    ########
    return HttpResponseRedirect(temp['url'])


def get_payment_result(request):  
    temp = GoldenPay(
        authKey = "", # goldenpay terefden verilir 
        paymentKey = ""
    ).getPaymentResult()

    # temp returnda xml qaytaracaq 

    return HttpResponse(temp)
    


