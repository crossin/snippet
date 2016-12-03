import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

#设置登录及服务器信息
mail_host = 'smtp.163.com'
mail_user = '159*****02'
mail_pass = '7******x'
sender = '159*****02@163.com'
receivers = ['7******0@qq.com']

#设置eamil信息
#添加一个MIMEmultipart类，处理正文及附件
message = MIMEMultipart()
message['From'] = sender
message['To'] = receivers[0]
message['Subject'] = 'title'
#推荐使用html格式的正文内容，这样比较灵活，可以附加图片地址，调整格式等
with open('abc.html','r') as f:
    content = f.read()
#设置html格式参数
part1 = MIMEText(content,'html','utf-8')
#添加一个txt文本附件
with open('abc.txt','r')as h:
    content2 = h.read()
#设置txt参数
part2 = MIMEText(content2,'plain','utf-8')
#附件设置内容类型，方便起见，设置为二进制流
part2['Content-Type'] = 'application/octet-stream'
#设置附件头，添加文件名
part2['Content-Disposition'] = 'attachment;filename="abc.txt"'
#添加照片附件
with open('1.png','rb')as fp:
    picture = MIMEImage(fp.read())
    #与txt文件设置相似
    picture['Content-Type'] = 'application/octet-stream'
    picture['Content-Disposition'] = 'attachment;filename="1.png"'
#将内容附加到邮件主体中
message.attach(part1)
message.attach(part2)
message.attach(picture)

#登录并发送
try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host,25)
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(sender,receivers,message.as_string())
    print('success')
    smtpObj.quit()
except smtplib.SMTPException as e:
    print('error',e)
