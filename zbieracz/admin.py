from django.contrib import admin
from zbieracz.models import Wpisy
from zbieracz.models import RSS


class WpisyAdmin(admin.ModelAdmin):
    # ...

    list_display = ('id', 'img_title', 'rss', 'pub_date', 'was_published_recently', 'img_src', 'img_our_src', 'img_our_src_small')

    list_display = ('img_title', 'rss', 'pub_date', 'was_published_recently', 'img_src', 'img_our_src', 'img_our_src_small')

    list_filter = ['pub_date']
    search_fields = ['img_title', 'img_alt']

admin.site.register(RSS)
admin.site.register(Wpisy, WpisyAdmin)