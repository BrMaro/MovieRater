from django.db import modelsclass Genre(models.Model):    name = models.CharField(max_length=100)    def __str__(self):        return self.nameclass Movie(models.Model):    title = models.CharField(max_length=100)    overview = models.TextField()    release_date = models.DateField(null=True, blank=True)    genres = models.ManyToManyField(Genre)    runtime = models.PositiveIntegerField()    revenue = models.DecimalField(max_digits=15, decimal_places=2)    budget = models.DecimalField(max_digits=15, decimal_places=2)    def __str__(self):        return self.title