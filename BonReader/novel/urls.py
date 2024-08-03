from django.urls import path
from . import views

urlpatterns = [
    # Noverls
    path("novels/", views.novel_list, name="novel_list"),
    path("novel/add/", views.add_novel, name="add_novel"),
    path("novel/<int:novel_id>/", views.novel_detail, name="novel_detail"),
    path("novel/<int:novel_id>/edit/", views.edit_novel_chapter, name="edit_novel"),
    path("novel/<int:novel_id>/delete/", views.delete_novel, name="delete_novel"),
    path("novel/<int:novel_id>/add_chapter/", views.add_chapter, name="add_chapter"),
    path(
        "novel/edit/<int:novel_id>/<int:chapter_id>/",
        views.edit_novel_chapter,
        name="edit_chapter",
    ),
    path(
        "novel/<int:novel_id>/<int:chapter_id>/delete/",
        views.delete_chapter,
        name="delete_chapter",
    ),
    # Shelf
    path("shelf/add_novel/", views.add_novel_to_shelf, name="add_novel_to_shelf"),
    path("shelf/novels/", views.get_shelf_novels, name="get_shelf_novels"),
    path("shelf/reading/", views.get_reading_novels, name="get_reading_novels"),
    path("shelf/completed/", views.get_completed_novels, name="get_completed_novels"),
]
