from django.contrib import admin

from apps.users.models import Users, Infor, UserAddress


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ["id", "username"]
    list_display_links = ["id", "username"]


@admin.register(Infor)
class InforAdmin(admin.ModelAdmin):
    list_display = ["id", "head", "nickname", "sex", "birthday", "school", "address", "hometown", "phone", "num"]
    list_display_links = ["id", "head", "nickname", "sex", "birthday", "school", "address", "hometown", "phone", "num"]


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "username", "phone", "hcity", "hproper", "harea", "brief", "isDefault"]
    list_display_links = ["id", "user", "username", "phone", "hcity", "hproper", "harea", "brief", "isDefault"]
