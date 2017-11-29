# app.py
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from config import BaseConfig
from flask import Flask, jsonify
from flask import request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from bot.botservice import BotService

from bot.botservice import parse_chat_id

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
service = BotService('423578322:AAECRbZkM5iS607zBXjeWnIJZXkFhIyl4wI')

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(func=service.get_updates,
                  trigger=IntervalTrigger(seconds=5),
                  id='updating_job',
                  name='Get updates from telegram',
                  replace_existing=True)
atexit.register(lambda: scheduler.shutdown())

from models import *

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/hello_world', methods=['GET', 'POST'])
def hello_world():
    return jsonify([{'msg': 'hello world'}])


# @app.route('/', methods=['GET', 'POST'])
@app.route('/get_updates', methods=['GET', 'POST'])
def get_updates():
    upd = service.get_updates()
    ids = parse_chat_id(upd)

    for id in ids:
        chat = Chat(id)
        db.session.merge(chat)

    db.session.commit()
    chats = Chat.query.all()
    return render_template('updates.html', chats=chats, status="All chat are loaded")


@app.route('/get_chats', methods=['GET', 'POST'])
def get_chats():
    return jsonify(list(service.chat_ids))


@app.route('/broadcast', methods=['GET', 'POST'])
def broadcast():
    message = request.args.get("msg") if request.args.get("msg") else None

    if message is None:
        return render_template('broadcast.html', status="What are you waiting for?")
    else:
        upd = service.get_updates()
        ids = parse_chat_id(upd)
        return render_template('broadcast.html', status="Message was sent to all chats")


@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    chat_id = request.args.get("chat") if request.args.get("chat") else None
    msg = request.args.get("msg") if request.args.get("msg") else None
    if chat_id is None or msg is None:
        return render_template('send_message.html', status="Need more data: text ot chat id")

    service.send_message(chat_id, msg)
    return render_template('send_message.html', status="Message was sent")


if __name__ == '__main__':
    app.run()
