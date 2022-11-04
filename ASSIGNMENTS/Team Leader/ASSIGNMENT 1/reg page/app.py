from flask import Flask,redirect,url_for,request
app=Flask(__name__)

@app.route('/success/<string:name>/<string:ml>/<string:pnm>') 
def success(name,ml,pnm):
   return "Welcome " + name +" !! <br><br> Your mail id is "+ml+" .<br><br> Your phone number is "+pnm


@app.route('/login',methods=['POST'])
def login():
    if request.method=='POST':
         user=request.form['nm'] 
         mailid=request.form['mail'] 
         phnum=request.form['num']

         return redirect(url_for('success',name=user,ml=mailid,pnm=phnum)) 
if __name__ ==' main ':
    app.run(debug=True)

