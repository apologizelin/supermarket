import hashlib
from django.shortcuts import redirect
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from market import settings


# 封装验证session的方法
def verify_login_required(func):
    """
    :param func: 传入的函数
    :return:
    """  # 登陆验证器

    def verify(request, *args, **kwargs):
        # 判断session中是否有ID,如果没有说明没有登录，请登录
        if request.session.get("ID") is None:
            # 配置文件中获取登录的URL地址
            return redirect("users:login")
        else:
            # 返回被调用函数
            return func(request, *args, **kwargs)

    return verify


# 加密方法
def set_password(password):
    # 新的加密字符串
    new_password = "{}{}".format(password, settings.SECRET_KEY)
    h = hashlib.md5(new_password.encode('utf-8'))
    return h.hexdigest()


# 登陆保存session的方法
def login(request, user):
    # 将用户id和手机号码,保存到session中
    request.session['ID'] = user.pk
    request.session.set_expiry(86400)
    request.session['username'] = user.username
    request.session.set_expiry(86400)
    # request.session['head'] = user.head
    # request.session.set_expiry(86400)


# 发送短信
def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    # 注意：不要更改
    REGION = "cn-hangzhou"
    PRODUCT_NAME = "Dysmsapi"
    DOMAIN = "dysmsapi.aliyuncs.com"
    # acs_client = AcsClient(const.ACCESS_KEY_ID, const.ACCESS_KEY_SECRET, REGION)
    acs_client = AcsClient(settings.ACCESSKEYID, settings.ACCESSKEYSECRET, REGION)
    region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)
    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)
    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)
    # 短信签名
    smsRequest.set_SignName(sign_name)
    # 数据提交方式
    # smsRequest.set_method(MT.POST)
    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)
    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)
    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)
    # TODO 业务处理
    return smsResponse
