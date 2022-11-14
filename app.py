from flask import Flask, request, jsonify, render_template
import os
# import requests
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('chatbot_page.html')


# run Flask app
if __name__ == '__main__':
    app.run()

