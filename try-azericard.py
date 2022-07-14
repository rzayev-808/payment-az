import requests

from payment.azericard import AzeriCard


class Coffee:
    def __init__(self, **kwargs) -> None:
        self.sugar = True

        self.antivirus = kwargs.get("antivirus", None)

        self.__dict__.update(**kwargs)


if __name__ == "__main__":
    obj = AzeriCard(
        AMOUNT="1",
        CURRENCY="AZN",
        ORDER="100001",  # order id si mininim 6 reqem olmalidi misal : 100001 : Order id olmadan script run olmur
        TERMINAL="123",  # bank terefinden verilir
        TRTYPE="1",  # Auth
        key_for_sign="",  # bank terefden onceden verilir
        DESC="",  # description
        MERCH_NAME="",  # magaza adi
        MERCH_URL="",  # callback sehifesi
        EMAIL="",  # emailiniz
        COUNTRY="AZ",
        BACKREF="",  # geri donus sehifesi
    )

    print(obj.bank_data())
    print(obj.test)

    malicious = {"virus": True}
    obj = Coffee(**malicious)
    print(obj.__dict__)
    print(obj.virus)
