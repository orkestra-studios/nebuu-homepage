#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, redirect, Response
from flup.server.fcgi import WSGIServer
from functools import wraps
from boto.s3.key import Key
from Queue import Queue
import time, boto, thread, os, smtplib, creds, email.utils
from email.mime.text import MIMEText

timestamp = lambda: int(time.time())
jobs = Queue()

AWS_ACCESS_KEY_ID = 'AKIAIYN4ARZAG5NOW4DQ'
AWS_SECRET_ACCESS_KEY = '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'

app = Flask(__name__,static_folder='static',static_url_path='/static')
conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

def check_auth(username, password):
    return username == 'admin' and password == '0020mojoA'

def authenticate():
    return Response(
    'Sayfayı görebilmeniz için giriş yapmanız gerekiyor', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/list')
@requires_auth
def listing():
    bucket = conn.create_bucket('video.nebuu.com',location=boto.s3.connection.Location.DEFAULT)
    link = lambda n: '<a href="http://video.nebuu.com/%s">%s</a>'%(n,n)
    keys = [link(k.name) for k in sorted(bucket.get_all_keys(),key=lambda e:e.last_modified,reverse=True)]
    return '<!doctype html><html><body>'+'<br/>'.join(keys)+'</body></html>'
   


def consume_uploads():
    while True:
        job = jobs.get()

        bucket = conn.create_bucket('video.nebuu.com',location=boto.s3.connection.Location.DEFAULT)

        k = Key(bucket)
        k.key = "%d_video_%s.m4v"%(job[0],timestamp())
        k.set_contents_from_filename('./%s'%job[1].name)
        k.set_acl("public-read")
        os.remove('./%s'%job[1].name)
        time.sleep(1)

@app.route('/upload/',methods=['POST'])
def upload():
    media = request.files['media']
    email = request.form['email']
    media.save('./%s'%media.name)
    jobs.put((email,media))
    return redirect('/#upload')

@app.route('/contact/',methods=['POST'])
def contact():
    #Connect to the SMTP server
    sender = smtplib.SMTP()
    sender.connect('smtp.gmail.com',587)
    #gmail auth methods
    sender.ehlo();sender.starttls();sender.ehlo()
    sender.login(creds.email,creds.password)
    try:
        body = "isim: %(name)s\nE-posta: %(email)s\n\n%(message)s"%request.form
        message = MIMEText(body,'plain','utf-8')
        message['To'] = email.utils.formataddr(('Recipient', 'alicanblbl@gmail.com'))
        message['From'] = email.utils.formataddr((request.form['name'], request.form['email']))
        message['Subject'] = 'NEBUU: %s'%request.form['subject']
        sender.sendmail(request.form['email'], ['alicanblbl@gmail.com','tanerman@gmail.com','ismailkok@orkestrayazilim.com','onur@orkestrayazilim.com'], message.as_string())
    finally:
      sender.quit()
    return redirect('/#contact')


if __name__ == '__main__':
    thread.start_new_thread(consume_uploads,())
    #app.run('0.0.0.0',8686,debug=True)
    WSGIServer(app).run() 
