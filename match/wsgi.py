# coding: utf-8

from manage import app

if __name__ == '__main__':
    app.debug = True
    app.run(host="120.77.57.126", port=8888)
