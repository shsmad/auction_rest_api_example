# -*- coding: utf-8 -*-

from application.application import create_app

application = create_app('app.cfg')

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=3000, debug=application.config.get('DEBUG'))
