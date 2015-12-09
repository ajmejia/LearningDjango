from django.contrib import admin

# Register your models here.
#---------------------------------------------------------------
#- Here I can tell django admin site that my models can have an
#- admin interface.
#---------------------------------------------------------------
from .models import Question


#---------------------------------------------------------------
#- I can customize what happens in the admin site, in particular
#- what happens with the models a registered by defining a
#- class.
#---------------------------------------------------------------
class QuestionAdmin(admin.ModelAdmin):
  fieldsets = [
               (None,               {'fields': ['question_text']}), #- I can group fields within div tags using this
                                                                    #- formatting. Can also define collapsed groups
               ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}), #- as in here.
              ]

admin.site.register(Question, QuestionAdmin)   #- Note that I had to add both instances of my question.
