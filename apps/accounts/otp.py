import pyotp,base64
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings



class OtpView:
    def __init__(self):
        pass

    def get_key(self,phonenumber,email=None):
        return str(phonenumber)+str(email)+str(datetime.date(datetime.now()))+"MEDMARKET_OTP_KEY"
    
    def get_otp(self,phonenumber,email=None):
        key=base64.b32encode(self.get_key(phonenumber,email).encode())
        otp=pyotp.TOTP(key,interval=settings.OTP_INTERVAL_TIME)
        self.send_otp(str(otp.now()),email)

        return otp.now()
    
    def validate_otp(self,otp,phonenumber,email=None):
        return self.get_otp(phonenumber,email)==otp
    
    def send_otp(self,otp,email):
        print("email sending ")
        subject ='MedMarket | Otp'
        message ='your Otp is {}.This will be valid up to 2 min only.'.format(otp)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['anand.pasam15@gmail.com',]
        try:
            send_mail(subject,message,email_from,recipient_list)
        except Exception as err:
            print(err)
            return False
        return True

    
