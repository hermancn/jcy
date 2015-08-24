from django.contrib import admin

# Register your models here.

from .models import SearchLog
from .models import DocumentLog

'''
class DocumentLogAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'access_time', 'site', 'document_id']
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'access_time', 'query', 'filter_query', 'start']


admin.site.register(SearchLog, SearchLogAdmin)
admin.site.register(DocumentLog, DocumentLogAdmin)
'''
