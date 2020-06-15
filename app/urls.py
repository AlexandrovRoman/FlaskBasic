import errors
import news
import organization as org
import users
from app import app

app.register_blueprint(news.bp)
app.register_blueprint(errors.bp)
app.register_blueprint(org.bp)
app.register_blueprint(users.bp)
