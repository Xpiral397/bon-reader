from django.urls import path
from . import views

urlpatterns = [
    # Novel URLs
    # List all novels
    path("novels/", views.novel_list, name="novel_list"),
    # Add a new novel
    path("novel/add/", views.add_novel, name="add_novel"),
    # Detail view of a specific novel by its ID
    path("novel/<int:novel_id>/", views.novel_detail, name="novel_detail"),
    # Edit a specific novel by its ID
    path("novel/<int:novel_id>/edit/", views.edit_novel_chapter, name="edit_novel"),
    # Delete a specific novel by its ID
    path("novel/<int:novel_id>/delete/", views.delete_novel, name="delete_novel"),
    # Add a chapter to a specific novel
    path("novel/<int:novel_id>/add_chapter/", views.add_chapter, name="add_chapter"),
    # Edit a specific chapter of a novel
    path(
        "novel/edit/<int:novel_id>/<int:chapter_id>/",
        views.edit_novel_chapter,
        name="edit_chapter",
    ),
    # Delete a specific chapter of a novel
    path(
        "novel/<int:novel_id>/<int:chapter_id>/delete/",
        views.delete_chapter,
        name="delete_chapter",
    ),
    # Review API URLs
    # List all reviews or create a new review
    path(
        "api/reviews/",
        views.ReviewViewSet.as_view({"get": "list", "post": "create"}),
        name="review-list",
    ),
    # Retrieve, update, or delete a specific review by its ID
    path(
        "api/reviews/<int:pk>/",
        views.ReviewViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="review-detail",
    ),
    # Shelf URLs
    # Add a novel to the shelf
    path("shelf/add_novel/", views.add_novel_to_shelf, name="add_novel_to_shelf"),
    # Get all novels on the shelf
    path("shelf/novels/", views.get_shelf_novels, name="get_shelf_novels"),
    # Get all novels currently being read
    path("shelf/reading/", views.get_reading_novels, name="get_reading_novels"),
    # Get all completed novels
    path("shelf/completed/", views.get_completed_novels, name="get_completed_novels"),
]
