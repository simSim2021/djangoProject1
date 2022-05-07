from django.contrib import admin

from .models import Option, Capital
from .models import Mark


admin.site.register(Capital)
admin.site.register(Option)
admin.site.register(Mark)

