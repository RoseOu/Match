# coding: utf-8

from flask import Flask, render_template
from app import app
from . import zhihu
from . import weibo
from . import wangyi
from . import douban
from . import getscore


@app.route('/', methods=['GET','POST'])
def index():
	return render_template("index.html")


