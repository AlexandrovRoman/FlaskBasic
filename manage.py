from Flask_DJ import manage
from Flask_DJ.app_init import add_urls
from app import app, config

"""database-methods: https://flask-migrate.readthedocs.io/en/latest/
db init - начало поддержки миграций
db migrate - миграция бд
db upgrade - обновление бд
db downgrade - откат миграции
some methods:
runserver - запуск сервера
startapp name - создание приложения name, возможно создания папки приложения с помощью флагов -t и -st
"""


# Кто удалит - у того рак яичка
# https://getbootstrap.com/2.3.2/components

# Выводит ОБЪЕКТЫ кадровиков и их пользователей, не удалять)
# global_init()
# session = create_session()
# user = session.query(User).filter(User.id == 2).first()
# print(user, user.personnel, user.users)

manage.init_manage_and_app(app)
manage.init_db_commands(config.models)

manage.manager.option("--templates", "-t", action="store_true")(
    manage.manager.option("--static", "-st", action="store_true")(
        manage.manager.option("name")(manage.startapp)))


@manage.manager.command
def runserver():
    add_urls(config.urlpatterns)
    manage.runserver(config.HOST, config.PORT)


manage.manager.run()
