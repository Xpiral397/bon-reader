from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Novel, Chapter, Shelf, ReadingActivity
from django.db.models import Q
from .serializers import NovelSerializer, NovelRankingSerializer, ChapterSerializer, ReadingActivity, ReadingActivitySerializer, ShelfSerializer
from django.shortcuts import get_object_or_404

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def novel_list(request):
    novels = Novel.objects.all()
    serializer = NovelSerializer(novels, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_novel(request):
    serializer = NovelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def novel_detail(request, novel_id):
    novel = get_object_or_404(Novel, id=novel_id)
    if request.method == 'GET':
        serializer = NovelSerializer(novel)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = NovelSerializer(novel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        novel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_chapter(request, novel_id):
    novel = get_object_or_404(Novel, id=novel_id)
    data = request.data
    data['novel'] = novel.id
    serializer = ChapterSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def edit_chapter(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    if request.method == 'PUT':
        serializer = ChapterSerializer(chapter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        chapter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ranking(request, ranking_type):
    if ranking_type not in ['power', 'trending', 'popular', 'active']:
        return Response({'error': 'Invalid ranking type'}, status=status.HTTP_400_BAD_REQUEST)

    if ranking_type == 'power':
        novels = Novel.objects.all().order_by('-ratings')  # Assuming 'ratings' indicates power
    elif ranking_type == 'trending':
        novels = Novel.objects.all().order_by('-views')  # Assuming 'views' indicates trending
    elif ranking_type == 'popular':
        novels = Novel.objects.all().order_by('-ratings')  # Assuming 'ratings' indicates popularity
    elif ranking_type == 'active':
        novels = Novel.objects.all().order_by('-chapters_count')  # Assuming 'chapters_count' indicates activity

    # Serialize the novel data
    serializer = NovelRankingSerializer(novels, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def genre_filter(request, genre=None, filter_by=None, sort_by=None):
    novels = Novel.objects.all()

    if genre:
        genres = genre.split(',')
        query = Q()
        for g in genres:
            query |= Q(genre__icontains=g)
        novels = novels.filter(query)

    if filter_by == 'completed':
        novels = novels.filter(completed=True)
    elif filter_by == 'not-completed':
        novels = novels.filter(completed=False)

    if sort_by == 'popular':
        novels = novels.order_by('-views')
    elif sort_by == 'recommended':
        novels = novels.order_by('-ratings')
    elif sort_by == 'rating':
        novels = novels.order_by('-ratings')
    elif sort_by == 'time-updated':
        novels = novels.order_by('-chapters__date_modified')
    else:
        novels = novels.order_by('-views')  # Default sort by popular if sort_by is not specified

    serializer = NovelSerializer(novels, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_novel_to_shelf(request):
    user = request.user
    novel_id = request.data.get('novel_id')
    shelf_name = request.data.get('shelf_name', 'Default Shelf')

    if not novel_id:
        return Response({'error': 'Novel ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        novel = Novel.objects.get(id=novel_id)
    except Novel.DoesNotExist:
        return Response({'error': 'Novel not found'}, status=status.HTTP_404_NOT_FOUND)

    shelf, created = Shelf.objects.get_or_create(user=user, name=shelf_name)
    ReadingActivity.objects.create(user=user, novel=novel, shelf=shelf)

    return Response({'message': 'Novel added to shelf'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_shelf_novels(request):
    user = request.user
    shelves = Shelf.objects.filter(user=user)
    serializer = ShelfSerializer(shelves, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reading_novels(request):
    user = request.user
    reading_activities = ReadingActivity.objects.filter(user=user, completed=False)
    serializer = ReadingActivitySerializer(reading_activities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_completed_novels(request):
    user = request.user
    completed_activities = ReadingActivity.objects.filter(user=user, completed=True)
    serializer = ReadingActivitySerializer(completed_activities, many=True)
    return Response(serializer.data)





