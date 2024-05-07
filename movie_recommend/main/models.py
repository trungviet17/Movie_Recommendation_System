from django.db import models

# Create your models here.



class Cast(models.Model): 

    name = models.CharField(max_length= 100)
    image = models.TextField()
    birthday = models.DateTimeField()
    bio = models.TextField()

class Movie(models.Model) : 

    title = models.CharField(max_length= 100)
    released = models.DateTimeField()
    overview = models.TextField()
    popularity = models.DecimalField(max_digits=5, decimal_places = 2)
    # image store link 
    image = models.TextField()
    genre = models.CharField(max_length = 200)
    casts = models.ManyToManyField(Cast)

    def __str__(self): 
        return self.title










