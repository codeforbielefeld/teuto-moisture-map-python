from mangum import Mangum

from .app import app

# Application for gunicorn etc.
app = app

# Handler for AWS
handler = Mangum(app)

