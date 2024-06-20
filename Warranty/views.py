from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.db import models
from .models import customer, product,repair
from .forms import (
registerForm,signinForm, ChangePasswordForm, CustomerForm, ProductForm,RepairtForm
)
from matplotlib.dates import DateFormatter
from io import BytesIO
import matplotlib.pyplot as plt
import urllib, base64
import datetime
import base64
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q, Count, F, Sum, When, Case, DecimalField
from django.db.models.functions import TruncMonth
from datetime import datetime
from django.shortcuts import render, redirect
from django.db import IntegrityError
from unidecode import unidecode
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
def home(request):
    return render(request, "Warranty/home.html")

def registerUser(request):
    if request.method == "POST":
        rF = registerForm(request.POST)
        if rF.is_valid():
            rF.save()
            lF = signinForm()
            return render(request, "Warranty/login.html", {"lF": lF})
        else:
            error_message = "Vui lòng kiểm tra lại thông tin đăng ký."
            return render(request, "Warranty/registerUser.html", {"rF": rF, "error_message": error_message})
    else:
        rF = registerForm()
        return render(request, "Warranty/registerUser.html", {"rF": rF})

class MyLoginView(View):
    def get(self, request):
        lF = signinForm
        return render(request, "Warranty/login.html", {"lF": lF})

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Sau khi đăng nhập thành công, chuyển hướng người dùng đến trang chính
            return redirect("Warranty:home")
        else:
            return render(
                request,
                "Warranty/login.html",
                {"lF": signinForm, "error_message": "Người dùng không tồn tại"},
            )


def logoutUser(request):
    logout(request)
    return render(request, "Warranty/login.html", {"lF": signinForm})

@login_required
def Change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password"]
            confirm_password = form.cleaned_data["confirm_password"]
            if user.check_password(old_password) and new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(
                    request, "Mật khẩu của bạn đã được thay đổi thành công!"
                )
                return render(request, "Warranty/home.html")  # Chuyển hướng đến trang hồ sơ của người dùng
            else:
                messages.error(
                    request,
                    "Vui lòng kiểm tra lại mật khẩu cũ và xác nhận mật khẩu mới.",
                )
        else:
            messages.error(request, "Vui lòng sửa các lỗi dưới đây.")
    else:
        form = ChangePasswordForm()
    return render(request, "Warranty/changepassword.html", {"form": form})

@login_required
def input_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            c_m = customer.objects.all()
            return render(request, "Warranty/CustomerInformation.html", {"c_m": c_m})  # Redirect to the customer information page after successfully inputting data
    else:
        form = CustomerForm()
    
    return render(request, 'Warranty/input_customer.html', {'c_f': form})

@login_required
def CustomerInformation(request):
    c_m = customer.objects.all()
    # Lấy số lượng thiết bị từ yêu cầu GET
    number_input = request.GET.get('numberInput')
    # Tạo queryset ban đầu và lọc các khách hàng có số lượng thiết bị bằng số được nhập
    if number_input:
        c_m = customer.objects.annotate(num_products=Count('product')).filter(num_products__exact=int(number_input))
    else:
        c_m = customer.objects.all()
    
    # Trả về template với danh sách khách hàng đã lọc
    return render(request, "Warranty/CustomerInformation.html", {"c_m": c_m })

@login_required
def edit_cu(request, customer_id):
    # Lấy thông tin của khách hàng từ ID được cung cấp
    m_m = customer.objects.get(id=customer_id)
    # Kiểm tra nếu phương thức yêu cầu là POST
    if request.method == "POST":
        # Tạo một biểu mẫu với dữ liệu đã gửi và thông tin khách hàng hiện có
        ad_f_m = CustomerForm(request.POST, instance=m_m)
        # Kiểm tra xem biểu mẫu có hợp lệ không
        if ad_f_m.is_valid():
            # Lưu biểu mẫu để cập nhật thông tin của khách hàng
            ad_f_m.save()
            # Chuyển hướng đến một trang thành công hoặc hiển thị một thông báo thành công
            return render(request,"Warranty/edit_cu.html",{"ad_f_m": ad_f_m, "error_message": "Thông tin cập nhật thành công"},)
        else:
            # Nếu biểu mẫu không hợp lệ, hiển thị lại biểu mẫu với các thông báo lỗi
            return render(request,"Warranty/edit_cu.html",{"ad_f_m": ad_f_m, "error_message": "Thông tin cập nhật không hợp lệ"},)
    else:
        ad_f_m = CustomerForm(instance=m_m)
    return render(request, "Warranty/edit_cu.html", {"ad_f_m": ad_f_m})

@login_required
def productInformation(request):
    # Lấy các tham số từ request
    requires_repair_param = request.GET.get("requires_repair")
    warranty_param = request.GET.get("warranty")
    # Tạo queryset ban đầu
    p_m = product.objects.all()

    # Xác định loại lọc và thực hiện lọc
    if requires_repair_param and warranty_param:
        if warranty_param == "warranty" and requires_repair_param == "repair":  # Lọc ra tất cả các sản phẩm
            p_m = p_m

        elif warranty_param == "warranty" and requires_repair_param == "Yes":   # Lọc ra các sản phẩm cần sửa chữa
            p_m = p_m.filter(repair__isnull=False)

        elif warranty_param == "warranty" and requires_repair_param == "No":    # Lọc ra các sản phẩm không cần sửa chữa
            p_m = p_m.filter(repair__isnull=True)

        elif warranty_param == "Active" and requires_repair_param == "repair":  # Lọc ra các sản phẩm còn bảo hành
            p_m = p_m.filter(warranty_product=1)

        elif warranty_param == "Active" and requires_repair_param == "Yes":    # Lọc ra các sản phẩm còn bảo hành và cần sửa chữa
            p_m = p_m.filter(warranty_product=1, repair__isnull=False)

        elif warranty_param == "Active" and requires_repair_param == "No":      # Lọc ra các sản phẩm còn bảo hành và không cần sửa chữa
            p_m = p_m.filter(warranty_product=1, repair__isnull=True)

        elif warranty_param == "Expired" and requires_repair_param == "repair": # Lọc ra các sản phẩm hết bảo hành
            p_m = p_m.filter(warranty_product=0)

        elif warranty_param == "Expired" and requires_repair_param == "Yes":    # Lọc ra các sản phẩm hết bảo hành và cần sửa chữa
            p_m = p_m.filter(warranty_product=0, repair__isnull=False)

        elif warranty_param == "Expired" and requires_repair_param == "No":     # Lọc ra các sản phẩm hết bảo hành và không cần sửa chữa
            p_m = p_m.filter(warranty_product=0, repair__isnull=True)
    
    # Trả về template với danh sách khách hàng đã lọc
    return render(request, "Warranty/productInformation.html", {"p_m": p_m})

@login_required
def edit_pro(request, product_id):
    # Lấy thông tin của khách hàng từ ID được cung cấp
    m_m = product.objects.get(id=product_id)
    # Kiểm tra nếu phương thức yêu cầu là POST
    if request.method == "POST":
        # Tạo một biểu mẫu với dữ liệu đã gửi và thông tin khách hàng hiện có
        ad_f_m = ProductForm(request.POST, instance=m_m)
        # Kiểm tra xem biểu mẫu có hợp lệ không
        if ad_f_m.is_valid():
            # Lưu biểu mẫu để cập nhật thông tin của khách hàng
            ad_f_m.save()
            # Chuyển hướng đến một trang thành công hoặc hiển thị một thông báo thành công
            return render(request,"Warranty/edit_pro.html",{"ad_f_m": ad_f_m, "error_message": "Thông tin cập nhật thành công"},)
        else:
            # Nếu biểu mẫu không hợp lệ, hiển thị lại biểu mẫu với các thông báo lỗi
            return render(request,"Warranty/edit_pro.html",{"ad_f_m": ad_f_m, "error_message": "Thông tin cập nhật không hợp lệ"},)
    else:
        ad_f_m = ProductForm(instance=m_m)
    return render(request, "Warranty/edit_pro.html", {"ad_f_m": ad_f_m})

@login_required
def input_warranty(request):
    if request.method == 'POST':
        p_f = ProductForm(request.POST)
        if p_f.is_valid():  # Change 'form' to 'p_f' here
            p_f.save()
            p_m = product.objects.all()
            return render(request, "Warranty/warrantyInformation.html", {"p_m": p_m})  # Redirect to the product information page after successfully inputting data
    else:
        p_f = ProductForm()  # Define 'p_f' here
    
    return render(request, 'Warranty/input_warranty.html', {'p_f': p_f})

@login_required
def warrantyInformation(request):
    # Retrieve query parameter from the URL
    requires_repair_param = request.GET.get("requires_repair")

    # Filter products based on the selected warranty status
    p_m = product.objects.all()

    if requires_repair_param :
        if requires_repair_param == "repair":  # Lọc ra tất cả các sản phẩm
            p_m = p_m

        elif requires_repair_param == "Yes":   # Lọc ra các sản phẩm cần sửa chữa
            p_m = p_m.filter(repair__isnull=False)

        elif requires_repair_param == "No":    # Lọc ra các sản phẩm không cần sửa chữa
            p_m = p_m.filter(repair__isnull=True)

    # Pass the filtered repairs to the template
    return render(request, 'Warranty/warrantyInformation.html', {'p_m': p_m})

@login_required
def input_repair(request):
    if request.method == 'POST':
        r_f = RepairtForm(request.POST)
        if r_f.is_valid():  # Change 'form' to 'p_f' here
            r_f.save()
            r_m = repair.objects.all()
            return render(request, "Warranty/repairInformation.html", {"r_m": r_m})  # Redirect to the product information page after successfully inputting data
    else:
        r_f = RepairtForm()
    return render(request, 'Warranty/input_repair.html', {'r_f': r_f})

@login_required
def repairInformation(request):
    # Retrieve query parameter from the URL
    warranty_status = request.GET.get('warranty')

    # Filter products based on the selected warranty status
    r_m = repair.objects.all()

    if warranty_status:
        if warranty_status == 'warranty':
            r_m = r_m
        elif warranty_status == 'Active':
            r_m = r_m.filter(product_id__warranty_product=1)
        elif warranty_status == 'Expired':
            r_m = r_m.filter(product_id__warranty_product=0)

    # Pass the filtered repairs to the template
    return render(request, 'Warranty/repairInformation.html', {'r_m': r_m})

@login_required
def edit_re(request, repair_id):
    # Lấy thông tin của khách hàng từ ID được cung cấp
    m_m = repair.objects.get(id=repair_id)
    # Kiểm tra nếu phương thức yêu cầu là POST
    if request.method == "POST":
        # Tạo một biểu mẫu với dữ liệu đã gửi và thông tin khách hàng hiện có
        ad_f_m = RepairtForm(request.POST, instance=m_m)
        # Kiểm tra xem biểu mẫu có hợp lệ không
        if ad_f_m.is_valid():
            # Lưu biểu mẫu để cập nhật thông tin của khách hàng
            ad_f_m.save()
            # Chuyển hướng đến một trang thành công hoặc hiển thị một thông báo thành công
            return render(request,"Warranty/edit_re.html",{"ad_f_m": ad_f_m, "error_message": "Thông tin cập nhật thành công"},)
        else:
            # Nếu biểu mẫu không hợp lệ, hiển thị lại biểu mẫu với các thông báo lỗi
            return render(request,"Warranty/edit_re.html",{"ad_f_m": ad_f_m, "error_message": "Thông tin cập nhật không hợp lệ"},)
    else:
        ad_f_m = RepairtForm(instance=m_m)
    return render(request, "Warranty/edit_re.html", {"ad_f_m": ad_f_m})

@login_required
def insearch(request):
    query = request.GET.get('q')
    
    c_m = customer.objects.filter(Q(name_customer__icontains=query))
    p_m = product.objects.filter(Q(name_product__icontains=query))
    
    # Kiểm tra xem có khách hàng hoặc sản phẩm nào được tìm thấy không
    if c_m.exists():
        return render(request, "Warranty/CustomerInformation.html", {"c_m": c_m})
    elif p_m.exists():
        return render(request, "Warranty/productInformation.html", {"p_m": p_m})
    else:
        # Nếu không tìm thấy khách hàng hoặc sản phẩm chính xác, chuyển hướng về trang chính
        return redirect("Warranty:home")
    