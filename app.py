
from flask import Flask, jsonify, render_template, request
from FacebookMonitor import FacebookMonitor

app = Flask(__name__)

access_token = 'EAANGamOm9fYBAK3V2XZAnTHJ6V1DmaN2zLl9XnmQanNq9xRZBm7a2XFZCygLNuZCgLpp6d8CnRVWqZBABzZBgcWNg5ZC0p4droKaZCD4e6rGwzaVlBQfgb8UbDrs2o5XSiDkZBYHAUvc0Xv7CaYuf3WvfATZAOjOqLJAT5XUvUv9tl1Iqk6lPXTSec3X4t7ZCuZCSNNVcucmvYUxWtzfe2fcgW0eMxcUdP3uocutdOYGv6UIigZArjfqNf0Ev'
group_id = '624356639516269'

fb_monitor = FacebookMonitor(access_token, group_id)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/scan_group_posts', methods=['GET', 'POST'])
def scan_group_posts():
    if request.method == 'POST':
        group_id = request.form.get('group_id')
        global fb_monitor
        fb_monitor = FacebookMonitor(access_token, group_id)
    result = fb_monitor.scan_group_posts()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)