from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=10, unique=True)
    nickname = models.CharField(max_length=10)
    email = models.EmailField(max_length=30, blank=True, null=True)
    profile_img = models.ImageField(upload_to='image/', default='image/user.png')
    financial_products = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    property = models.IntegerField(blank=True, null=True)
    annual_salary = models.IntegerField(blank=True, null=True)

    USERNAME_FIELD = 'username'

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        from allauth.account.utils import user_email, user_field, user_username

        data = form.cleaned_data
        username = data.get("username")
        nickname = data.get("nickname")
        email = data.get("email")
        profile_img = data.get("profile_img")
        financial_product = data.get("financial_products")
        age = data.get("age")
        property = data.get("property")
        annual_salary = data.get("annual_salary")

        user_email(user, email)
        user_username(user, username)
        if nickname:
            user_field(user, "nickname", nickname)
        if profile_img:
            user.profile_img = profile_img
        if age:
            user.age = age
        if property:
            user.property = property
        if annual_salary:
            user.annual_salary = annual_salary
        if financial_product:
            financial_products = user.financial_products.split(',') if user.financial_products else []
            financial_products.append(financial_product)
            user_field(user, "financial_products", ','.join(financial_products))
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        return user
