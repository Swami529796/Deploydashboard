import app
project_home = u'/home/swami52979/Deploydashboard'
if project_home not is sys.path:
    sys.path = [project_home] + sys.path

from app import app
application = app.server
