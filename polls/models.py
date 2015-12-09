from django.db import models

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

class Choice(models.Model):
  question = models.ForeignKey(Question)             #- The ForeignKey tells django that each Choice is related
                                                     #- to a single Question (many-to-one).
  choice_text = models.CharField(max_length=200)     #- Another CharField
  votes = models.IntegerField(default=0)             #- An IntegerField with default value of 0.
