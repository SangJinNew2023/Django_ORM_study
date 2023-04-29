from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("category", views.CategoryViewSet, basename="category") #{basename} - The base to use for the URL names that are created.
router.register("comments", views.CommentViewSet, basename="comments")
router.register("likes", views.LikeViewSet, basename="likes")
router.register("posts", views.PostViewSet, basename="posts")

urlpatterns = router.urls
#DefaultRouter() includes routes for the standard set of list, create, retrieve, update, partial_update and destroy actions,
#but additionally includes a default API root view
