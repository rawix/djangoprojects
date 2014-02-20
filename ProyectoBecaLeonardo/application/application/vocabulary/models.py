from django.db import models

# ------------------------------------------------------------------------------
#                               Vocabulary class.
# ------------------------------------------------------------------------------

class Vocabulary(models.Model):
    unit = models.CharField(max_length=3);  
    title = models.TextField(max_length=200);
    word = models.CharField(max_length=200);
    acronym = models.CharField(max_length=200);
    description = models.TextField();
    link = models.URLField();
    image = models.URLField();

	# Alphabetical Order  
    class Meta:
        verbose_name_plural = u'Vocabulary'
        ordering = ['word']

    def __unicode__(self):
        return str(self.unit) + " - " + self.word;


