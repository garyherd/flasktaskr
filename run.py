# run.py


import os
from project import app
from project._config import DEBUG

host = '0.0.0.0'
port = int(os.environ.get('PORT', 5000))

if DEBUG == True:
    app.run()
else:
    app.run(host=host, port=port)


