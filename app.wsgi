# -*- coding: utf-8 -*-

import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from application.application import create_app

application = create_app('app.cfg')

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=3000, debug=application.config.get('DEBUG'))
