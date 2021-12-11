from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class MyUserManager(BaseUserManager):
    def create_user(self,full_name,phonenumber,email,password=None,admin=False,staff=False,email_verify=False,active=False):
        if not full_name:
            raise ValueError(_("Please Enter Full Name !."))

        if not phonenumber:
            raise ValueError(_("Please Enter Mobile Number !."))

        if not email:
            raise ValueError(_("Please Enter Email !."))

        if not password:
            raise ValueError(_("Please Enter Password !."))

        user=self.model(email=self.normalize_email(email),
                        full_name=full_name,
                        phonenumber=phonenumber,
                        admin=admin,
                        staff=staff,
                        active=active,
                        email_verify=email_verify
                        )

        user.set_password(password)

        user.save(using=self._db)

        return user
    def create_superuser(self,full_name,phonenumber,email,password=None,admin=True,staff=True,email_verify=False,active=True):
        user=self.create_user(full_name,phonenumber,email,password,admin,staff,email_verify,active)

        user.save(using=self._db)

        return user
    
    def create_staffuser(self,full_name,phonenumber,email,password=None,admin=False,staff=True,email_verify=False,active=False):
        user=self.create_user(full_name,phonenumber,email,password,admin,staff,email_verify,active)

        user.save(using=self._db)

        return user


