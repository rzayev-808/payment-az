import asyncio
from email.message import EmailMessage
import itertools
import aiosmtplib


class Async:
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    def async_loop(f):
        def decorated(self, *args, **kwargs):
            self.loop.run_until_complete(f(self, *args, **kwargs))
        return decorated

    @async_loop
    async def function(self, *args, **kwargs):
        message = EmailMessage()
        message["From"] = kwargs.get('sender'),
        message["To"] = kwargs.get('to'),
        message["Subject"] = "Payment result"
        message.set_content(kwargs.get('content'))
        await aiosmtplib.send(
            message,
            hostname=kwargs.get('hostname'),
            port=kwargs.get('port'),
            username=kwargs.get('username'),
            password=kwargs.get('password'),
            use_tls=True
            )
