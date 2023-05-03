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

        #데이터 생성
        obj = Category.objects.create(
            title=title_data, slug=slug_data, description=description_data,
        )
        serializer = self.serializer_class(obj)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])  # post만 허용
    def save_data(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data or None)
        data.is_valid(raise_exception=True)

        title_data = data.validated_data.get("title")
        slug_data = data.validated_data.get("slug")
        description_data = data.validated_data.get("description")

        obj = Category() #model
        obj.title = title_data
        obj.slug = slug_data
        obj.description = description_data
        obj.save()

        serializer = self.serializer_class(obj)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @action(detail=False, methods=['POST'])  # post만 허용
    def get_or_create_data(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data or None)
        data.is_valid(raise_exception=True)

        title_data = data.validated_data.get("title")
        slug_data = data.validated_data.get("slug")

        obj, _ = Category.objects.get_or_create(title=title_data, slug=slug_data)

        serializer = self.serializer_class(obj)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])  # post만 허용
    def bulk_create_data(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data or None, many=True) #many=True시리얼라이저가 값이 여러개라고 인식을 해서 list 형태로 반환
        data.is_valid(raise_exception=True)

        new_data=[]

        for row in data.validated_data:
            new_data.append(
                Category(
                    title=row["title"],
                    slug=row["slug"],
                    description=row["description"],
                )
            )
        if new_data:
            new_data = Category.objects.bulk_create(new_data)

        # serializer = self.serializer_class(new_data) #여러개의 데이터 생성시는 이부분은 삭제하고 Response에 serializer.data는 메세지로 대체

        return Response("Successfully created data", status=status.HTTP_201_CREATED)

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
#many=True 를 설정해주면 시리얼라이저가 값이 여러개라고 인식을 해서 list 형태로 반환을 해준다