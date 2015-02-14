from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/photos/')
def photos():
	return render_template('photos.html')

@app.route('/photos/<int:photo_id>')
def display_photo(photo_id):
	return render_template('display_photo.html', photo_id=photo_id)

@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == '__main__':
	app.run()