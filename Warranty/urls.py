from django.urls import path, include
from . import views

app_name = "Warranty"
urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.MyLoginView.as_view(), name="login"),
    path("registerUser/", views.registerUser, name="registerUser"),
    path("logoutUser/", views.logoutUser, name="logoutUser"),
    path("change_password/", views.Change_password, name="change_password"),
    path("input_customer/", views.input_customer, name="input_customer"),
    path("CustomerInformation.", views.CustomerInformation, name="CustomerInformation"),
    path("productInformation/", views.productInformation, name="productInformation"),    
    path("input_warranty/", views.input_warranty, name="input_warranty"),
    path("warrantyInformation/", views.warrantyInformation, name="warrantyInformation"),
    path("input_repair/", views.input_repair, name="input_repair"),
    path("repairInformation.", views.repairInformation, name="repairInformation"),
    path('insearch/', views.insearch, name='insearch'),
    path("edit_cu/<int:customer_id>/", views.edit_cu, name="edit_cu"),
    path("edit_pro/<int:product_id>/", views.edit_pro, name="edit_pro"),
    path("edit_re/<int:repair_id>/", views.edit_re, name="edit_re"),
]
