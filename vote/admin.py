from django.contrib import admin
from vote.models import County, Constituency, Ward, Voter

# Register your models here.

admin.site.register(County)
admin.site.register(Constituency)
admin.site.register(Ward)
admin.site.register(Voter)
