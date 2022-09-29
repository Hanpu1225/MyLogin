from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import form
import hashlib  #映入哈希表的库

# Create your views here.
def index(request):
    pass
    return render(request,'login/index.html')

def login(request):

    if request.session.get('is_login',None): #通过session会话，要求不能重复登录
        return redirect('/index/')

    if request.method=="POST":
        login_form = form.UserForm(request.POST)  #创建表单
        message = '验证码输入错误，请重新输入'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')  # 从用户表单中获取数据
            password = login_form.cleaned_data.get('password')  #login_form.cleaned_data字典中读取所有的表单数据，
            try:
                user = models.User.objects.get(name=username) #models.User.objects.get从数据库中取数据
            except:
                message = '用户不存在！！！'
                return render(request,'login/login.html',locals())
            if user.password==password:   #使用Hash库进行密码加密
                request.session['is_login'] =True #往session中写入注册状态
                request.session['user_id'] = user.id #往session中写入用户id
                request.session['user_name'] = user.name #往session中用户名
                return redirect('/index/')
            else:
                message = '密码错误，请仔细检查！！！'
                return render(request,'login/login.html',locals())
    login_form = form.UserForm()
    return render(request,'login/login.html',locals())

def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = form.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = form.RegisterForm()
    return render(request, 'login/register.html', locals())

def logout(request):
    if not request.session.get('is_login',None): #若没有登录
        return redirect('/login/')
    request.session.flush() #一次性将session记录的文件删除
    return redirect('/login/')


def hash_code(s,salt='Mylogin'):
    h = hashlib.sha3_256()
    s+=salt
    h.update(s.encode())
    return h.hexdigest()