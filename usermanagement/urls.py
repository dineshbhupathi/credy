from django.conf.urls import url
from . import views
urlpatterns = [
    url('users',views.CreateUserAPIView.as_view()),
    url('movies/',views.MoviesList),
    url('collection/(?P<collection_uuid>[0-9a-f-]*)',views.Collections.as_view()),
    url('requests-count/', views.requestcount),
    url('api/v1/movie',views.LocalMovies.as_view()),
    url('save/',views.feed_data.as_view()),


]