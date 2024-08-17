from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q, Avg
from rest_framework import viewsets
from drf_yasg import openapi
from .models import Novel, Review, Shelf, ReadingActivity
from .serializers import (
    NovelCreateSerializer,
    NovelSerializer,
    NovelEditSerializer,
    NovelRankingSerializer,
    ChapterSerializer,
    ReadingActivitySerializer,
    ShelfSerializer,
    ReviewSerializer,
)


# @swagger_auto_schema(
#     method='get',
#     operation_description="Retrieve a list of all novels",
#     responses={200: NovelSerializer(many=True)}
# )
@api_view(["GET"])
def novel_list(request):
    novels = Novel.objects.all()
    serializer = NovelSerializer(novels, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method="post",
    operation_description="Add a new novel",
    request_body=NovelCreateSerializer,
    responses={201: NovelSerializer, 400: "Bad Request"},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_novel(request):
    serializer = NovelCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(
#     method='post',
#     operation_description="Edit a chapter within a novel",
#     request_body=ChapterSerializer,
#     responses={200: ChapterSerializer, 400: "Bad Request"}
# )
@api_view(["POST"])
def edit_novel_chapter(request, novel_id, chapter_id):
    novel = get_object_or_404(Novel, id=novel_id)
    chapter = get_object_or_404(novel.chapters, id=chapter_id)
    serializer = ChapterSerializer(chapter, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(
#     method='get',
#     operation_description="Retrieve detailed information about a novel",
#     responses={200: NovelSerializer}
# )
@api_view(["GET"])
def novel_detail(request, novel_id):
    novel = get_object_or_404(Novel, id=novel_id)
    serializer = NovelSerializer(novel)
    return Response(serializer.data)


# @swagger_auto_schema(
#     method='delete',
#     operation_description="Delete a novel",
#     responses={204: "No Content", 404: "Not Found"}
# )
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_novel(request, novel_id):
    novel = get_object_or_404(Novel, id=novel_id, user=request.user)
    novel.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# @swagger_auto_schema(
#     method='post',
#     operation_description="Add a new chapter to a novel",
#     request_body=ChapterSerializer,
#     responses={201: ChapterSerializer, 400: "Bad Request"}
# )
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_chapter(request, novel_id):
    novel = get_object_or_404(Novel, id=novel_id)
    title = request.data.get("title")
    novel.add_new_chapter(title)
    serializer = ChapterSerializer(novel.chapters, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# @swagger_auto_schema(
#     method='delete',
#     operation_description="Delete a chapter from a novel",
#     responses={204: "No Content", 404: "Not Found"}
# )
@api_view(["DELETE"])
def delete_chapter(request, novel_id, chapter_id):
    novel = get_object_or_404(Novel, id=novel_id)
    chapter = get_object_or_404(novel.chapters, id=chapter_id)
    novel = Novel.objects.get(id=novel_id)
    novel.chapters_count -= 1
    novel.save()
    chapter.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# @swagger_auto_schema(
#     method='get',
#     operation_description="Get a ranking of novels based on different criteria",
#     manual_parameters=[
#         openapi.Parameter('ranking_type', openapi.IN_PATH, description="Type of ranking (power, trending, popular, active)", type=openapi.TYPE_STRING)
#     ],
#     responses={200: NovelRankingSerializer(many=True), 400: "Bad Request"}
# )
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_ranking(request, ranking_type):
    if ranking_type not in ["power", "trending", "popular", "active"]:
        return Response(
            {"error": "Invalid ranking type"}, status=status.HTTP_400_BAD_REQUEST
        )

    if ranking_type == "power":
        novels = Novel.objects.all().order_by("-ratings")
    elif ranking_type == "trending":
        novels = Novel.objects.all().order_by("-views")
    elif ranking_type == "popular":
        novels = Novel.objects.all().order_by("-ratings")
    elif ranking_type == "active":
        novels = Novel.objects.all().order_by("-chapters_count")

    serializer = NovelRankingSerializer(novels, many=True)
    return Response(serializer.data)


# @swagger_auto_schema(
#     method='get',
#     operation_description="Filter novels by genre, completion status, and sorting",
#     manual_parameters=[
#         openapi.Parameter('genre', openapi.IN_QUERY, description="Comma-separated list of genres to filter by", type=openapi.TYPE_STRING, required=False),
#         openapi.Parameter('filter_by', openapi.IN_QUERY, description="Filter novels by completion status (completed, not-completed)", type=openapi.TYPE_STRING, required=False),
#         openapi.Parameter('sort_by', openapi.IN_QUERY, description="Sort novels by popularity, recommendation, rating, or time updated", type=openapi.TYPE_STRING, required=False),
#     ],
#     responses={200: NovelSerializer(many=True)}
# )
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def genre_filter(request, genre=None, filter_by=None, sort_by=None):
    novels = Novel.objects.all()

    if genre:
        genres = genre.split(",")
        query = Q()
        for g in genres:
            query |= Q(genre__icontains=g)
        novels = novels.filter(query)

    if filter_by == "completed":
        novels = novels.filter(completed=True)
    elif filter_by == "not-completed":
        novels = novels.filter(completed=False)

    if sort_by == "popular":
        novels = novels.order_by("-views")
    elif sort_by == "recommended":
        novels = novels.order_by("-ratings")
    elif sort_by == "rating":
        novels = novels.order_by("-ratings")
    elif sort_by == "time-updated":
        novels = novels.order_by("-chapters__date_modified")
    else:
        novels = novels.order_by("-views")

    serializer = NovelSerializer(novels, many=True)
    return Response(serializer.data)


# @swagger_auto_schema(
#     method='post',
#     operation_description="Add a novel to a user's shelf",
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'novel_id': openapi.Schema(type=openapi.TYPE_INTEGER),
#             'shelf_name': openapi.Schema(type=openapi.TYPE_STRING, default="Default Shelf")
#         },
#         required=['novel_id']
#     ),
#     responses={201: "Novel added to shelf", 400: "Bad Request", 404: "Novel not found"}
# )
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_novel_to_shelf(request):
    user = request.user
    novel_id = request.data.get("novel_id")
    shelf_name = request.data.get("shelf_name", "Default Shelf")

    if not novel_id:
        return Response(
            {"error": "Novel ID is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        novel = Novel.objects.get(id=novel_id)
    except Novel.DoesNotExist:
        return Response({"error": "Novel not found"}, status=status.HTTP_404_NOT_FOUND)

    shelf, created = Shelf.objects.get_or_create(user=user, name=shelf_name)
    ReadingActivity.objects.create(user=user, novel=novel, shelf=shelf)
    return Response({"message": "Novel added to shelf"}, status=status.HTTP_201_CREATED)


# @swagger_auto_schema(
#     method='get',
#     operation_description="Get all novels on a user's shelves",
#     responses={200: ShelfSerializer(many=True)}
# )
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_shelf_novels(request):
    user = request.user
    shelves = Shelf.objects.filter(user=user)
    serializer = ShelfSerializer(shelves, many=True)
    return Response(serializer.data)


# @swagger_auto_schema(
#     method='get',
#     operation_description="Get novels currently being read by the user",
#     responses={200: ReadingActivitySerializer(many=True)}
# )  7
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_reading_novels(request):
    user = request.user
    reading_activities = ReadingActivity.objects.filter(user=user, completed=False)
    serializer = ReadingActivitySerializer(reading_activities, many=True)
    return Response(serializer.data)


# @swagger_auto_schema(
#     method='get',
#     operation_description="Get novels completed by the user",
#     responses={200: ReadingActivitySerializer(many=True)}
# )
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_completed_novels(request):
    user = request.user
    reading_activities = ReadingActivity.objects.filter(user=user, completed=True)
    serializer = ReadingActivitySerializer(reading_activities, many=True)
    return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(detail=True, methods=["get"])
    def average_rating(self, request, pk=None):
        # Get the average rating for the specified novel
        reviews = Review.objects.filter(novel_id=pk)
        average_rating = reviews.aggregate(Avg("rating"))["rating__avg"]
        return Response({"average_rating": average_rating})

    @action(detail=True, methods=["get"])
    def list_reviews(self, request, pk=None):
        # List all reviews for the specified novel
        reviews = Review.objects.filter(novel_id=pk)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
