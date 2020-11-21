from django.conf.urls import url
from . import views
urlpatterns = [
    url('register/',views.CreateUserAPIView.as_view()),
    url('movies/',views.MoviesList),
    url('collection/(?P<collection_uuid>[0-9a-f-]*)',views.Collections.as_view()),
    url(r'^requests-count/$', views.requestcount),
    # url(r'^requests-count/reset/$', views.requestcount_reset),

]