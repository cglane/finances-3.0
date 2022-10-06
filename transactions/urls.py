from django.conf.urls import include
from django.contrib import admin
from transactions import views
from django.urls import include, re_path

api_patterns = [
    re_path(r"^sheets_list/$", views.sheets_list, name="sheets_list"),
    re_path(r"^add_data", views.UpdateData.as_view()),
    re_path(r"^authorize", views.Authorize.as_view()),
    re_path(r"^read_csv", views.ReadCSV.as_view()),
]
urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(
        r"^api/v1/",
        include((api_patterns, "rest_framework"), namespace="rest_framework"),
    ),
]
