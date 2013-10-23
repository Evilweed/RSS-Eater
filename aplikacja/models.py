from django.db import models

# Create your models here

class Dribble(models.Model):
	pub_date = models.DateTimeField('date published')
	votes = models.IntegerField()
	art_link = models.CharField(max_length=300)
	img_our_src = models.CharField(max_length=300)
	img_cdn_src = models.CharField(max_length=300)
	img_src = models.CharField(max_length=300)
	img_alt = models.CharField(max_length=100)
	img_title = models.CharField(max_length=100)

	def __unicode__(self):
		return self.img_title


