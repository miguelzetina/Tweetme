from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from tweets.views import TweetListView
from .views import home

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TweetListView.as_view(), name="home"),
    url(r'^tweet/', include('tweets.urls', namespace="tweet")),
    url(r'^api/tweet/', include('tweets.api.urls', namespace="tweet-api")),
]

if settings.DEBUG:
    urlpatterns += (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
