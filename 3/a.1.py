import os, sys
try:
	from flask import Flask, render_template, request, jsonify, send_from_directory
except:
	os.system("pip3 install --user flask")
	from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)



@app.route('/')
def main():
	return render_template('1.html', result="asdsadasd")


UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '//'
# app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
app.config['DOWNLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__)) + '//'

@app.route('/', methods = ['GET', 'POST'])
def post():
	if request.method=='POST' and 'file' in request.files:
		if request.files['file'].filename != '':
			post_file(request.files['file'])
	if request.method=='POST' and 'text' in  request.form:
		if request.form['text'] != '':
			print(request.form['text'])
			return render_template('1.html',result=request.form['text'])
	return main()


@app.route('/search_pill', methods=['POST'])
def search_pill():
	category = request.form['category']
	current_page = int(request.form['current_page'])
	## Search in your database and send back the serialized object.
	return jsonify(result = [p.serialize() for p in project_list])



def post_file(_file):
	_secure_filename = secure_filename(_file.filename)
	_file.save(os.path.dirname(os.path.abspath(__file__))+'//'+_secure_filename)
	#os.system('python %s//0bcfb5fc630d380718066bb7d22f5629.py %s//%s' %(sys.path[0],sys.path[0],_secure_filename))
	#return send_from_directory(app.config['DOWNLOAD_FOLDER'], 'trans.'+_secure_filename, as_attachment=True)
	return

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8080,debug=True)

