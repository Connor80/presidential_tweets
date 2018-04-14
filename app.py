from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    start = datetime.date(2017, 1, 20)
    today = datetime.date.today()
    diff = today - start
    day = diff.days
    return render_template('layout.html', day=day)

if __name__ == "__main__":
    app.run(debug=True)
