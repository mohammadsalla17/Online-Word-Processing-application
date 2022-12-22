from django.urls import path

from . import views, apis

urlpatterns = [
    # views
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('account/', views.account, name='account'),
    path("edit/<int:file_id>/", views.edit, name='edit'),
    path('logout/', views.logout, name='logout'),

    # apis
    path("user/", apis.user, name='user'),
    path("create/", apis.create, name='create'),
    path("save/<int:file_id>/", apis.save, name='save'),
    path("delete/<int:file_id>/", apis.delete, name='delete'),
    path("rename/<int:file_id>/", apis.rename, name='rename'),
]
