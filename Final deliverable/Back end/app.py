from glob import escape

import ibm_db
import re
from newsapi import NewsApiClient
import pycountry

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)

hostname = 'b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud'
uid = 'qbc77613'
pwd = 'Ih7n42kjzJRpuViC'
driver = "{IBM DB2 ODBC DRIVER}"
db_name = 'Bludb'
port = '31249'
protocol = 'TCPIP'
cert = "certi.crt"
dsn = (
    "DATABASE ={0};"
    "HOSTNAME ={1};"
    "PORT ={2};"
    "UID ={3};"
    "SECURITY=SSL;"
    "PROTOCOL={4};"
    "PWD ={6};"
).format(db_name, hostname, port, uid, protocol, cert, pwd)
connection = ibm_db.connect(dsn, "", "") 
app.secret_key = 'a'

@app.route('/')

def login():
    return render_template('signin.html')

@app.route('/signin.html',methods = ['POST'])

def getUser():
    if request.method == 'POST':
        user = request.form['uname']
        password = request.form['upwd']
        sql = "SELECT * FROM CUSTOMER1 where Email = ?"
        stmt = ibm_db.prepare(connection, sql)
        email = user
        # Explicitly bind parameters
        ibm_db.bind_param(stmt, 1,user)
        ibm_db.execute(stmt)
        dictionary = ibm_db.fetch_assoc(stmt)
        pwd = dictionary["PASSWORD"]
        if password != pwd:
            return render_template('error.html')
        
        return render_template('base.html')
    

@app.route('/signup.html')

def putUser():
    return render_template('signup.html')   

@app.route('/signup.html',methods = ['POST'])

def storedUser():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        mail = request.form['mail']
        npwd = request.form['npwd']
        cpwd = request.form['cpwd']

        
        print("inside checking")
        
        if len(fname) == 0 or len(lname) == 0 or len(mail) == 0 or len(npwd)== 0 or len(cpwd) == 0:
            msg = "Form is not filled completely!!"
            print(msg)
            return render_template('signup.html', msg=msg)
        elif npwd != cpwd:
            msg = "Password is not matched"
            print(msg)
            return render_template('signup.html', msg=msg)
        
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', mail):
            msg = 'Invalid email'
            print(msg)
            return render_template('signup.html', msg=msg)
        elif not re.match(r'[A-Za-z]+', fname):
            msg = "Enter valid Firstname"
            print(msg)
            return render_template('signup.html', msg=msg)
        elif not re.match(r'[A-Za-z]+', lname):
            msg = "Enter valid LastName"
            print(msg)
            return render_template('signup.html', msg=msg)
        sql = "select * from CUSTOMER1 where email = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 3, mail)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Acccount already exists'
        else:
            mail = mail
        

        sql = "INSERT INTO CUSTOMER1 (FirstName,LastName,Email,password,confirmpassword) VALUES(?,?,?,?,?);"
        stmt = ibm_db.prepare(connection, sql)
        ibm_db.bind_param(stmt, 1, fname)
        ibm_db.bind_param(stmt, 2, lname)
        ibm_db.bind_param(stmt, 3, mail)
        ibm_db.bind_param(stmt, 4, npwd)
        ibm_db.bind_param(stmt, 5, cpwd)
        ibm_db.execute(stmt)
        print("successs")
        msg = "succesfully signed up"
        return render_template('signin.html', msg=msg, name=name)
    else:
        return render_template('signup.html')
           

@app.route('/forpass.html')

def get_User():
    return render_template('forpass.html') 
@app.route('/change pass.html')

def get_User1():
    return render_template('change pass.html') 

@app.route('/home1.html',methods = ['POST','GET'])
def home():
    api_key = 'f9ea965541334519819e9b3275eb54f8'
    
    newsapi = NewsApiClient(api_key=api_key)
    

    top_headlines = newsapi.get_top_headlines(sources = "bbc-news")
    all_articles = newsapi.get_everything(sources = "bbc-news")

    t_articles = top_headlines['articles']
    a_articles = all_articles['articles']

    news = []
    desc = []
    img = []
    p_date = []
    url = []

    for i in range (len(t_articles)):
        main_article = t_articles[i]

        news.append(main_article['title'])
        desc.append(main_article['description'])
        img.append(main_article['urlToImage'])
        p_date.append(main_article['publishedAt'])
        url.append(main_article['url'])

        contents = zip( news,desc,img,p_date,url)

    news_all = []
    desc_all = []
    img_all = []
    p_date_all = []   
    url_all = []

    for j in range(len(a_articles)): 
        main_all_articles = a_articles[j]   

        news_all.append(main_all_articles['title'])
        desc_all.append(main_all_articles['description'])
        img_all.append(main_all_articles['urlToImage'])
        p_date_all.append(main_all_articles['publishedAt'])
        url_all.append(main_article['url'])
        
        all = zip( news_all,desc_all,img_all,p_date_all,url_all)

    return render_template('home1.html',contents=contents,all = all)
   



    


if __name__ == '__main__':
 
   
    app.run(debug=True)
