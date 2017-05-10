# send mail after workflow finished
  
def send_complete_mail(mail_to,sub,content): 
    import smtplib  
    from email.mime.text import MIMEText  
    mail_host='smtp.gmail.com:587'
    mail_user="proteome.firmiana"
    mail_pass="email password"
    mail_postfix="gmaiil.com"
    
    mail_from="Firmiana"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')  
    msg['Subject'] = sub  
    msg['From'] = mail_from  
    msg['To'] = mail_to  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host) 
        server.starttls() 
        server.login(mail_user,mail_pass)  
        server.sendmail(mail_from, mail_to, msg.as_string())  
        server.quit()  
        print 'Send mail success'
        return True  
    except Exception, e:  
        print 'Send mail failed\n'+str(e)  
        return False 