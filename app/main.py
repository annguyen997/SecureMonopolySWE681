from flask import Flask, render_template, flash,make_response, redirect,render_template,request
from forms import LoginForm,RegisterForm
from driver import Driver 
import socket
import sys

def sendToController(data):
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect(("127.0.0.1",2004))
	clientSocket.send(data.encode())
	dataFromServer = clientSocket.recv(1024)
	return(dataFromServer.decode())


app = Flask(__name__)
app.config['SECRET_KEY'] = 'derp_derp'

@app.route("/")
def default():
    return render_template('base.html', title='Welcome')
@app.route("/index")
def index():
    return render_template('base.html', title='Welcome')


@app.route('/new_game', methods=['GET', 'POST'])
def new_game():
	if(request.method == 'GET' and 'sessionID' in request.cookies and 'userName' in request.cookies):
		print(request.cookies)
		output=sendToController('{"mana_":["createGame"],"username_": "'+request.cookies.get('userName')+'","sessionID_":"'+request.cookies.get('sessionID')+'"}')
		return render_template('text_noform.html', title="You're good!", message=output)
		#{"mana_":["createGame"],"username_": "Hoa_test1","sessionID_":"TFdcXBlITLFyCAUsI7hSOxuAHZdfFYj1oVDmYvqItwY="}
	else:
		return render_template('text_noform.html', title="You're good!", message="Please login or create an account")


@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		 output=sendToController('{"user_": ["Create","'+request.form['username']+'","'+request.form['password']+'"]}')
		 #print(output)
		 #output=registration.createUser(request.form['username'],request.form['password'])
		 resp=make_response(render_template('text_noform.html', title="You're good!", message="Registration successful, logged in with token: "+output))
		 resp.set_cookie('sessionID',output)
		 resp.set_cookie('userName',request.form['username'])
		 return resp
	if request.method == 'GET':
	    form = RegisterForm()
	    if form.validate_on_submit():
	        flash('Login requested for user {}'.format(
	            form.username.data))
	        return redirect('/index')
	    return render_template('registration.html', title='Register', form=form)	


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		 output=sendToController('{"user_": ["Authenticate","'+request.form['username']+'","'+request.form['password']+'"]}')
		 #print(output)
		 #output=registration.createUser(request.form['username'],request.form['password'])
		 resp=make_response(render_template('text_noform.html', title="You're good!", message="Authentication successful, logged in with token: "+output))
		 resp.set_cookie('sessionID',output)
		 resp.set_cookie('userName',request.form['username'])
		 return resp
	if request.method == 'GET':
	    form = LoginForm()
	    if form.validate_on_submit():
	        flash('Login requested for user {}'.format(
	            form.username.data))
	        return redirect('/index')
	    return render_template('login.html', title='Sign In', form=form)


if __name__ == "__main__":
    app.run(host='127.0.0.1',port='8443',debug=True,ssl_context='adhoc')
