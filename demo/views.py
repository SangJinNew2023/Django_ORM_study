from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Comment, Like, Post
from .serializers import CategorySerializer, CommentSerializer, LiketSerializer, PostSerializer
# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['POST'])  # post만 허용
    def create_data(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data or None)
        data.is_valid(raise_exception=True)

        title_data = data.validated_data.get("title")
        slug_data = data.validated_data.get("slug")
        description_data = data.validated_data.get("description")

        # DB에 데이터 생성
        obj = Category.objects.create(
            title=title_data, slug=slug_data, description=description_data,
        )
        serializer = self.serializer_class(obj)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LiketSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# The actions provided by the ModelViewSet class are .list(), .retrieve(), .create(), .update(), .partial_update(), and .destroy().
#@action decorator:modelviewset을 쓰면서 기본 기능 외에 추가 기능 구현
#detail=설정을 통해 pk값의 지정여부 결정,True는 url:/{prefix}/{pk}, False는 url:/{prefix}/ 형태로 맵핑
#The serializer class that should be used for validating and deserializing input,
# and for serializing output. Typically, you must either set this attribute, or override the get_serializer_class() method.
#.is_valid(raise_exception=True)는 유요성 에러 발생시 HTTP 400 Bad Rquest 응답
#data.validated_data.get("title")는 data의 validated된 데이터 중 'title'인 데이터만 get