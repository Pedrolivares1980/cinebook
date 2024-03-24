from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    tmdb_id = models.IntegerField(unique=True, verbose_name="TMDb ID")
    director = models.CharField(max_length=255, verbose_name="Director")
    cast = models.TextField(verbose_name="Cast") 
    user_rating = models.FloatField(verbose_name="User Rating")
    trailer_link = models.URLField(verbose_name="Trailer Link")
    overview = models.TextField(verbose_name="Overview")
    release_date = models.DateField(verbose_name="Release Date")
    poster_path = models.URLField(verbose_name="Poster URL")
    original_language = models.CharField(max_length=10, verbose_name="Original Language")


    def __str__(self):
        return self.title

    def user_rating_stars(self):
        # Convierte la calificación del 1-10 a 1-5
        rating_scaled = self.user_rating / 2  # Escala de 1-10 a 1-5
        rating_rounded = round(rating_scaled * 2) / 2  # Redondea al múltiplo más cercano de 0.5
        return rating_rounded

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"