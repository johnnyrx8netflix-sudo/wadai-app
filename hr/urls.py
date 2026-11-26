from django.urls import path
from . import views

urlpatterns = [
    path("skill-sheet/", views.skill_sheet_apply, name="skill_sheet_apply"),
    path("skill-sheet/list/", views.skill_sheet_list, name="skill_sheet_list"),
    path("skill-sheet/<int:pk>/", views.skill_sheet_detail, name="skill_sheet_detail"),
    path("api/postal-lookup/", views.postal_lookup, name="postal_lookup"),
]