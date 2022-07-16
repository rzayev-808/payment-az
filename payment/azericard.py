import hashlib
import random
from typing import Dict, Tuple

import requests

from payment import utils
from payment.invoice import Async


class OrderMissingException(Exception):
    def __init__(
        self, message: str = 'ORDER attributunu qeyd etmək lazımdır. məs: "100001"'
    ):
        self.message = message
        super().__init__(self.message)


class AzeriCard:
    MERCH_GMT = "+4"

    def __init__(self, *args, **kwargs):
        order = kwargs.get("ORDER", None)

        if order is not None:
            self.__dict__.update(**kwargs)
        else:
            raise OrderMissingException()

    def bank_data(self):
        data = self.__dict__
        data["p_sign"] = self.generate_p_sign(data)
        return self.send_data(**data)

    def send_data(self, *args, **kwargs):
        url = "https://mpi.3dsecure.az/cgi-bin/cgi_link"
        response = requests.post(url, data=kwargs)
        return response.text

    def callback(self, *args, **kwargs):
        convert = kwargs
        convert["TRTYPE"] = ("21",)
        irand = random.randint(1, 10000000)
        nonce = utils.substr(hashlib.md5(str(irand).encode("utf-8")).hexdigest(), 0, 16)
        oper_time = utils.gmdate("%Y%m%d%H%I%S")
        t = "21"
        to_sign = (
            str(len(convert["ORDER"]))
            + convert["ORDER"]
            + str(len(convert["AMOUNT"]))
            + convert["AMOUNT"]
            + str(len(convert["CURRENCY"]))
            + convert["CURRENCY"]
        )
        (
            +str(len(convert["RRN"]))
            + convert["RRN"]
            + str(len(convert["INT_REF"]))
            + convert["INT_REF"]
            + str(len(t))
            + str(t)
            + str(len(convert["TERMINAL"]))
        )
        (
            +convert["TERMINAL"]
            + str(len(oper_time))
            + str(oper_time)
            + str(len(nonce))
            + str(nonce)
        )
        res = utils.hex2bin(convert["key_for_sign"])
        convert["p_sign"] = utils.hash_hmac("sha1", to_sign, res)
        print(convert)
        return self.send_data(**kwargs)

    def data_result(self, *args, **kwargs):
        kwargs["send_email"] = False
        if kwargs["ACTION"] == "0":
            check = self.callback(**kwargs)
            if kwargs["send_email"] == True:
                send_mail = Async()
                send_mail.function(
                    port=kwargs.get("port"),
                    hostname=kwargs.get("hostname"),
                    password=kwargs.get("password"),
                    sender=kwargs.get("sender"),
                    to=kwargs.get("to"),
                    content=kwargs.get("content"),
                )
            if check == "0":
                return {"status": "Ugurlu əməliyyat", "action": kwargs["ACTION"]}
            if check == "1":
                return "Duplicate transaction detected;"
            if check == "2":
                return "Transaction declined;"
            if check == "3":
                return "Transaction processing fault."
        elif kwargs["ACTION"] == "RC":
            return "Error" + "" + kwargs["ACTION"]

    def reversal(self, *args, **kwargs):
        convert = kwargs
        convert["TRTYPE"] = "22"
        irand = random.randint(1, 10000000)
        nonce: str = utils.substr(
            hashlib.md5(str(irand).encode("utf-8")).hexdigest(), 0, 16
        )
        oper_time: str = utils.gmdate("%Y%m%d%H%I%S")
        to_sign = (
            str(len(convert["AMOUNT"]))
            + convert["AMOUNT"]
            + str(len(convert["CURRENCY"]))
            + convert["CURRENCY"]
            + str(len(convert["RRN"]))
            + convert["RRN"]
            + str(len(convert["INT_REF"]))
            + convert["INT_REF"]
            + str(len(convert["TRTYPE"]))
            + convert["TRTYPE"]
            + str(len(convert["TERMINAL"]))
            + convert["TERMINAL"]
            + str(len(oper_time))
            + oper_time
            + str(len(nonce))
            + nonce
        )
        res = utils.hex2bin(convert["key_for_sign"])
        convert["p_sign"] = utils.hash_hmac("sha1", to_sign, res)
        check = self.send_data(**kwargs)
        if check == "0":
            return {"status": "Ugurlu əməliyyat", "action": kwargs["ACTION"]}
        if check == "1":
            return "Duplicate transaction detected;"
        if check == "2":
            return "Transaction declined;"
        if check == "3":
            return "Transaction processing fault."

    def generate_to_sign(self, data: Dict[str, str]) -> str:
        random_integer = random.randint(1, 10000000)
        nonce: str = utils.substr(
            hashlib.md5(str(random_integer).encode("utf-8")).hexdigest(), 0, 16
        )
        oper_time: str = utils.gmdate("%Y%m%d%H%I%S")
        to_sign = (
            str(len(data["AMOUNT"]))
            + data["AMOUNT"]
            + str(len(data["CURRENCY"]))
            + data["CURRENCY"]
            + str(len(data["ORDER"]))
            + data["ORDER"]
            + str(len(data["DESC"]))
            + data["DESC"]
            + str(len(data["MERCH_NAME"]))
            + data["MERCH_NAME"]
            + str(len(data["MERCH_URL"]))
            + data["MERCH_URL"]
            + str(len(data["TERMINAL"]))
            + data["TERMINAL"]
            + str(len(data["EMAIL"]))
            + data["EMAIL"]
            + str(len(data["TRTYPE"]))
            + data["TRTYPE"]
            + str(len(data["COUNTRY"]))
            + data["COUNTRY"]
            + str(len(self.MERCH_GMT))
            + self.MERCH_GMT
            + str(len(oper_time))
            + str(oper_time)
            + str(len(nonce))
            + str(nonce)
            + str(len(data["BACKREF"]))
            + data["BACKREF"]
        )

        return to_sign

    def generate_p_sign(self, data: Dict[str, str]) -> str:
        to_sign: str = self.generate_to_sign(data)
        binary_key: bytes = utils.hex2bin(data["key_for_sign"])
        return utils.hash_hmac("sha1", to_sign, binary_key)
