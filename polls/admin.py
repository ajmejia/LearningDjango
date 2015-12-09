from django.contrib import admin

# Register your models here.
#---------------------------------------------------------------
#- Here I can tell django admin site that my models can have an
#- admin interface, as follows:
#---------------------------------------------------------------
from .models import Question

admin.site.register(Question)
