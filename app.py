from flask import Flask

import views



app = Flask(__name__)

app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/result', view_func=views.result, methods=['POST'])

if __name__ == '__main__':
    app.run()