from django.urls import path

from .views import register, login, kb_query, usage_summary

urlpatterns = [

    path(
        "auth/register/",
        register,
        name="register",
    ),

    path(
        "auth/login/",
        login,
        name="login",
    ),
    path("kb/query/", kb_query, name="kb_query"),
    path(
    "admin/usage-summary/",
    usage_summary,
    name="usage-summary",
),
]