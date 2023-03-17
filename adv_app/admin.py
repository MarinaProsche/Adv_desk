from django.contrib import admin
from .models import User, Adv, Reply, Author, Media


admin.site.register(Adv)
admin.site.register(Reply)
admin.site.register(Author)
admin.site.register(Media)

# Register your models here.
