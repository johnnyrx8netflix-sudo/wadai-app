from django.urls import path
from . import views

urlpatterns = [
    path("skill-sheet/", views.skill_sheet_apply, name="skill_sheet_apply"),
    path("api/postal-lookup/", views.postal_lookup, name="postal_lookup"),
]