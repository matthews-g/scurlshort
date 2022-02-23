from urlshortener.views import ShortenUrl, GetCodeStats, GetShortCode
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shorten/', ShortenUrl.as_view(), name='shorten_url'),
    path('<str:short_code>/', GetShortCode.as_view(), name='short_code'),
    path('<str:short_code>/stats/', GetCodeStats.as_view(), name='short_code_stats'),
]

urlpatterns = format_suffix_patterns(urlpatterns)