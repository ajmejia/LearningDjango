from django.contrib import admin

# Register your models here.
#---------------------------------------------------------------
#- Here I can tell django admin site that my models can have an
#- admin interface.
#---------------------------------------------------------------
from .models import Choice, Question


#---------------------------------------------------------------
#- I can customize what happens in the admin site, in particular
#- what happens with the models a registered by defining a
#- class.
#---------------------------------------------------------------
class ChoiceInline(admin.TabularInline):
  model = Choice
  extra = 3                                                          #- This way I can add a bunch of choices at once.

class QuestionAdmin(admin.ModelAdmin):
  fieldsets = [
               (None,               {'fields':  ['question_text']}), #- I can group fields within div tags using this
                                                                     #- formatting. Can also define collapsed groups
               ('Date information', {'fields':  ['pub_date'],
                                     'classes': ['collapse']}),      #- as in here.
              ]
  inlines = [ChoiceInline]                                           #- Plus, the choices will be added/edited in the
                                                                     #- question page.
  list_display = ('question_text', 'pub_date',
                  'was_published_recently')                          #- Select the columns to display in the list
                                                                     #- page.
  list_filter = ['pub_date']                                         #- Adding filter by datetime of publication.
  search_fields = ['question_text']                                  #- Adding search capabilities.

#admin.site.register(Choice)

admin.site.register(Question, QuestionAdmin)   #- Note that I had to add both instances of my question.
