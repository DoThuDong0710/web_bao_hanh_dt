from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import customer, product, repair

from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import User
import re

from django import forms
from django.contrib.auth.models import User
import re

class registerForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput)
    store_code = forms.CharField(max_length=10)  # Thêm trường Mã cửa hàng

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Mật khẩu không khớp")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not re.match(r"^\w+$", username):
            raise forms.ValidationError("Tài khoản chứa ký tự đặc biệt")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Tài khoản đã tồn tại")

    def clean_store_code(self):
        store_code = self.cleaned_data.get("store_code")
        if store_code != "CD2002":
            raise forms.ValidationError("Mã cửa hàng không hợp lệ")
        return store_code

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"]
        )
        user.save()
        return user



class signinForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

class ChangePasswordForm(forms.Form):
    Mật_khẩu_cũ = forms.CharField(max_length=20, widget=forms.PasswordInput)
    Mật_khẩu_mới = forms.CharField(max_length=20, widget=forms.PasswordInput)
    Nhập_lại_mật_khẩu_mới = forms.CharField(max_length=20, widget=forms.PasswordInput)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = ['name_customer', 'address_customer', 'phone_number_customer', 'email_customer']
        labels = {
            'name_customer': 'Tên',
            'address_customer': 'Địa chỉ',
            'phone_number_customer': 'Số điện thoại',
            'email_customer': 'Email'
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ['customer_id', 'Manufacturer_product','name_product', 'purchase_date', 'warranty_period']
        labels = {
            'customer_id': 'Khách hàng',
            'Manufacturer_product': 'Hãng sản xuất',
            'name_product': 'Tên thiết bị',
            'purchase_date': 'Ngày mua',
            'warranty_period': 'Thời gian bảo hành',
        }
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }

class RepairtForm(forms.ModelForm):
    class Meta:
        model = repair
        fields = [ 'product_id', 'fault_status', 'start_date', 'end_date']
        labels = {
            'product_id':'Thiết bị',
            'fault_status': 'Tình trạng hư hỏng',
            'start_date': 'Ngày bắt đầu bảo hành',
            'end_date': 'Ngày kết thúc bảo hành',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }