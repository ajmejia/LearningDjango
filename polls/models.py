import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
#---------------------------------------------------------------
#- Models are the definitions of the data my application will
#- handle. Each model is a class (table in the database) and
#- each model will have some attributes (fileds in the table)
#- which will define the type of data and its behaviour.
#-
#- They will inherite from the Model class which defines a set
#- of properties and methods to handle the several datatypes.
#-
#- The code below will allow django to:
#-    * Create the database holding the app data.
#-    * Create the python handles to access that database.
#---------------------------------------------------------------
class Question(models.Model):
  question_text = models.CharField(max_length=200)   #- max_length is mandatory.
  pub_date = models.DateTimeField("date published")  #- First positional arg handles the human-readable name
                                                     #- of the field. This defaults to the name of the
                                                     #- variable in machine-readable format.
  def __unicode__(self):
    return self.question_text                        #- A human-readable representation of the Question object.

  def was_published_recently(self):                  #- Another method for handling publication date (?).
    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

                                                                   #- This is probably telling how to treat this method
                                                                   #- as a field. Like a custom field.
  was_published_recently.admin_order_field = 'pub_date'            #- Custom order field when request ordering by this one.
  was_published_recently.boolean = True                            #- Tells the renderer this is a boolean field.
  was_published_recently.short_description = 'Published recently?' #- Short human-readable name.

class Choice(models.Model):
  question = models.ForeignKey(Question)             #- The ForeignKey tells django that each Choice is related
                                                     #- to a single Question (many-to-one).
  choice_text = models.CharField(max_length=200)     #- Another CharField
  votes = models.IntegerField(default=0)             #- An IntegerField with default value of 0.

  def __unicode__(self):
    return self.choice_text
