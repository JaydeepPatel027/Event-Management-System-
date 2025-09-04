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


# ✅ Event Images (slideshow for each category)
class EventImage(models.Model):
    id = models.AutoField(primary_key=True)
    event_category = models.ForeignKey(EventCategory, related_name="images", on_delete=models.CASCADE, db_column="event_category_id")
    photo_url = models.CharField(max_length=500)

    def __str__(self):
        return f"Image for {self.event_category.event_name}"

    class Meta:
        db_table = 'event_images'
        managed = False



class EventService(models.Model):
    service_id = models.AutoField(primary_key=True)
    event = models.ForeignKey(EventCategory, on_delete=models.CASCADE, related_name="services")
    service_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.event.event_name} - {self.service_name}"
    
    class Meta:
        db_table = 'event_services'
        managed = False

class EventGallery(models.Model):
    gallery_id = models.AutoField(primary_key=True)
    event_id = models.IntegerField()
    event_type = models.CharField(max_length=255)
    image_links = models.TextField()  # assuming it stores URLs

    class Meta:
        db_table = 'event_gallery'
        managed = False
        
class ServiceOption(models.Model):
    option_id = models.AutoField(primary_key=True)
    service = models.ForeignKey(EventService, on_delete=models.CASCADE, related_name='options')
    option_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    photo_url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.option_name

    class Meta:
        db_table = 'service_options'
        managed = False
