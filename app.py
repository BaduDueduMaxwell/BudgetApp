from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def expense():
    return render_template('settings.html')


if __name__ == '__main__':
    app.run(debug=True)
