from flask import Flask, render_template
import web_map
app = Flask(__name__)


@app.route('/')
@app.route('/main/')
def main():
    return render_template('map.html')


if __name__ == '__main__':
    web_map.render_html()
    app.run(debug=True)
