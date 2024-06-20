from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class customer(models.Model):
    id = models.AutoField(primary_key=True)
    name_customer = models.CharField(max_length=100, null=False, blank=False)
    address_customer = models.CharField(max_length=1000, null=False, blank=False)
    phone_number_customer = models.CharField(max_length=10,unique=True,blank=True,null=True)
    email_customer = models.CharField(max_length=30)
    def __str__(self):
        return self.name_customer
    @property
    def ds_product(self):
        return product.objects.filter(customer_id=self.id)


class product(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(customer, on_delete=models.CASCADE)
    Manufacturer_product = models.CharField(max_length=100, null=False, blank=False)
    name_product = models.CharField(max_length=100, null=False, blank=False)
    purchase_date = models.DateField()
    warranty_period_CHOICES = ((12, '12 months'),(24, '24 months'))
    warranty_period = models.IntegerField(choices=warranty_period_CHOICES)
    warranty_status_CHOICES = ((0, 'Hết bảo hành'),(1, 'Còn bảo hành'))
    warranty_product = models.IntegerField(choices=warranty_status_CHOICES, null=True, blank=True) 

    def save(self, *args, **kwargs):
        # Cập nhật warranty_product dựa trên purchase_date và warranty_period
        if self.purchase_date + timedelta(days=self.warranty_period * 30) < timezone.now().date():
            self.warranty_product = 0
        else:
            self.warranty_product = 1

        super().save(*args, **kwargs)
    
    def clean(self):
        super().clean()
        if self.purchase_date and self.purchase_date > timezone.now().date():
            raise ValidationError(_('Purchase date cannot be in the future.'))
        
    def warranty(self):
        if self.warranty_product == 1:
            return "Còn bảo hành"
        else:
            return "Hết bảo hành"
        
    def repair_status(self):
        if self.repair_set.exists():
            return "Đang sửa chữa"
        else:
            return "Không sửa chữa"
        
    @property
    def repair_pro(self):
        return repair.objects.filter(product_id=self.id)
    
    def __str__(self):
        return self.name_product

from django.core.exceptions import ValidationError    

class repair (models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    fault_status = models.CharField(max_length=1000, null=True, blank=True)  # Tình trạng hư hỏng
    start_date = models.DateField(null=True, blank=True)  # Ngày bắt đầu bảo hành
    end_date = models.DateField(null=True, blank=True)  # Ngày kết thúc bảo hành
 
    def clean(self):
        super().clean()

        if self.start_date and self.start_date > timezone.now().date():
            raise ValidationError(_('Start date cannot be in the future.'))
        if self.start_date and self.start_date < self.product_id.purchase_date:
            raise ValidationError(_('Start date cannot be before purchase date.'))
        if self.end_date and self.end_date < self.product_id.purchase_date:
            raise ValidationError(_('End date cannot be before purchase date.'))
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError(_('Start date cannot be after end date.'))
    @property
    def Customer_id(self):
        return self.product_id.customer_id
    def __str__(self):
        return self.fault_status