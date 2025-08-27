from django.db import models

# Create your models here.
class client_details(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'client_details'   # table name
        managed = False   

    
class EventCategory(models.Model):  
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=100)
    event_description = models.TextField()
    photo_url = models.CharField(max_length=255)

    def __str__(self):
        return self.event_name
    
    class Meta:
        db_table = 'event_categories'
        managed = False
