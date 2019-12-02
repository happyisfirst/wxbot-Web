import os
from threading import Thread

import auth
import wechat
#from wechat import bot, dir_path, wechat_main
from database import db
from flask import Flask, render_template, redirect, url_for


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'development key'

    # @app.route("/")
    # def index():
    #    return redirect(url_for("auth.login"))

    # register the database commands
    #from db import db

    db.init_app(app)

    # apply the blueprints to the app
    #from flaskr import auth, blog

    app.register_blueprint(auth.bp)
    app.register_blueprint(wechat.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    #app.add_url_rule("/", endpoint="index")
    return app


if __name__ == '__main__':
    app = create_app()
    start_info = wechat.bot.load_login_status(wechat.dir_path + '/itchat.pkl')
    if start_info:
        thread = Thread(target=wechat.wechat_main, daemon=True, args=(start_info,))
        thread.start()

    app.run(host="0.0.0.0")
