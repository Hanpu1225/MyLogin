import os
from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'MyLogin.settings'

if __name__ == 'main':

    send_mail(
        '来自www.SDT.com的测试邮件',
        '欢迎访问www.SDT.com，这里是SDT软件教程站点，本站专注于Python、Django和JAVA技术的分享！',
        '1076294884@qq.com',
        ['hanpu1225@163.com'],
    )