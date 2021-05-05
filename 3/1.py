import os, sys
try:
   from flask import Flask, render_template, request, jsonify, send_from_directory
except:
   os.system("pip3 install --user flask")
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)

@app.route('/')
def main():
   return render_template('1.html')

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8080,debug=True)

