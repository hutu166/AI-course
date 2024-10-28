from flask import Flask
from chat import views as chat_views
from system import views as system_views
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # globally enable CORS

app.config['SECRET_KEY'] = 'secret1234'

app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'

app.register_blueprint(chat_views.chat_bp, url_prefix='/chat')
app.register_blueprint(system_views.system_bp, url_prefix='/')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5500', threaded=True, debug=False)
