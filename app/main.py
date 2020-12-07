from flask import Flask, render_template, flash, redirect,render_template,request
from forms import LoginForm,RegisterForm
from driver import Driver 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'derp_derp'

@app.route("/")
def default():
    return render_template('base.html', title='Welcome')
@app.route("/index")
def index():
    return render_template('base.html', title='Welcome')


@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		 registration = Driver()
		 output=registration.createUser(request.form['username'],request.form['password'])
		 return render_template('text_noform.html', title="You're good!", message=output)
	if request.method == 'GET':
	    form = RegisterForm()
	    if form.validate_on_submit():
	        flash('Login requested for user {}'.format(
	            form.username.data))
	        return redirect('/index')
	    return render_template('registration.html', title='Register', form=form)	


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(
            form.username.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)


if __name__ == "__main__":
    app.run(host='127.0.0.1',port='8443',debug=True,ssl_context='adhoc')