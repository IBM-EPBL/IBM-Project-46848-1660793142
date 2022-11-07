from flask import Flask, render_template
app = Flask(__name__)
@app.route('/',methods=["GET","POST"])
def index():
    return render_template('index.html')
@app.route('/Blog')
def blog():
    return render_template('blog.html')
@app.route('/Signup')
def signup():
    return render_template('signup.html')
@app.route('/Signin')
def signin():
    return render_template('signin.html')
if __name__=='__main__':
    app.run(debug=True)