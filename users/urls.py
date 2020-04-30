from app import api
from organization.views import personnel_department
from utils.urls import relative_path
from .api import UserListResource, UserResource
from .views import profile, login, logout, \
    edit_profile, personnel, education, notification, registration, t2, confirm_email, change_password, restore_password

urlpatterns = [
    relative_path('profile/', profile),
    relative_path('profile/redact/', edit_profile, methods=['GET', 'POST']),
    relative_path('login/', login, methods=['GET', 'POST']),
    relative_path('logout/', logout),
    relative_path('profile/personnel/', personnel),
    relative_path('education/', education),
    relative_path('profile/notification/', notification),
    relative_path('profile/menu_organization/personnel_department/', personnel_department, methods=['GET', 'POST']),
    relative_path('registration/', registration, methods=["GET", "POST"]),
    relative_path('restore/', restore_password, methods=["GET", "POST"]),
    relative_path('forgot/<email>/<token>/', change_password, methods=["GET", "POST"]),
    relative_path('confirm/', confirm_email),
    relative_path('profile/t2/', t2)
]

api.add_resource(UserListResource, '/api/user')
api.add_resource(UserResource, '/api/user/<int:user_id>')
