from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path(
        "dashboard/fragment/memelist/",
        views.MemeListFragmentView.as_view(),
        name="meme_list_fragment",
    ),
    path("dashboard/meme/create", views.MemeCreateView.as_view(), name="meme_create"),
    path(
        "dashboard/meme/create/fragment/suggested-tags",
        views.MemeCreateSuggestedTagsView.as_view(),
        name="meme_create_suggested_tags",
    ),
    path(
        "dashboard/meme/<uuid:uuid>/update",
        views.MemeUpdateView.as_view(),
        name="meme_update",
    ),
    path(
        "dashboard/meme/<uuid:uuid>/delete",
        views.MemeDeleteView.as_view(),
        name="meme_delete",
    ),
    path(
        "dashboard/meme/<uuid:uuid>/content",
        views.MemeContentView.as_view(),
        name="meme_content",
    ),
]
