from flask import Flask
from flask import url_for
from flask import render_template
from markupsafe import escape

app = Flask(__name__)


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

if __name__ == "__main__":
    app.run()