import pyotp,base64
from datetime import datetime
from django.conf import settings



class OtpView:
    def __init__(self):
        pass

    def get_key(self,phonenumber,email=None):
        return str(phonenumber)+str(email)+str(datetime.date(datetime.now()))+"MEDMARKET_OTP_KEY"
    
    def get_otp(self,phonenumber,email=None):
        key=base64.b32encode(self.get_key(phonenumber,email).encode())
        otp=pyotp.TOTP(key,interval=settings.OTP_INTERVAL_TIME)
        return otp.now()
    
    def validate_otp(self,otp,phonenumber,email=None):
        return self.get_otp(phonenumber,email)==otp
    
