from flask import Flask, render_template, g, abort, request, session, url_for, flash, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku

# DEBUG = True
SECRET_KEY = 'a secret'
USERNAME = 'galen'
PASSWORD = 'admin'

WELCOME_IMAGE = 2

app = Flask(__name__)
app.config.from_object(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/photos'
heroku =Heroku(app)
db = SQLAlchemy(app)

@app.route('/')
def index():
	return render_template('index.html', photo=get_photo(WELCOME_IMAGE))

@app.route('/photos/')
def photos():
	dbOut = Photo.query.all()
	photos = [dict(id=photo.id, title=photo.title, url=photo.url) \
		for photo in dbOut]
	return render_template('photos.html', photos=photos)

@app.route('/photos/<int:photo_id>')
def display_photo(photo_id):
	photo = get_photo(photo_id)
	if photo is None:
		flash('Photo not found.')
		return redirect(url_for('photos'))
	else:
		return render_template('display_photo.html', photo=photo)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/add', methods=['GET', 'POST'])
def add_photo():
	if request.method == 'POST':
		if not session.get('logged_in'):
			abort(401)
		title = request.form['title']
		caption = request.form['caption']
		url = request.form['url']
		photo = Photo(title, caption, url)
		db.session.add(photo)
		db.session.commit()
		flash('Photo was added succesfully!')
		return redirect(url_for('photos'))
	else:
		return(render_template('add_photo.html'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid Username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid Password'
		else:
			session['logged_in'] = True
			flash('You were logged in succesfully!')
			return redirect(url_for('photos'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out succesfully!')
	return redirect(url_for('index'))


class Photo(db.Model):
	__tablename__ = "photos"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120))
	caption = db.Column(db.String(1000))
	url = db.Column(db.String(500))

	def __init__(self, title, caption, url):
		self.title = title
		self.caption = caption
		self.url = url

	def __repr__(self):
		return '<Photo %r>' % self.title

def init_db():
	db.create_all()

def get_photo(photo_id):
	# Returns a dict containing the the fields for photo_id.
	photo = Photo.query.get(photo_id)
	if photo is None: return None
	return dict(title=photo.title, caption=photo.caption, url=photo.url)

if __name__ == '__main__':
	app.run

