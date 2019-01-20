from django.db import models
from ckeditor.fields import RichTextField
from django_extensions.db.fields import AutoSlugField
from files.models import S3File

# Create your models here.


# class Baseitem(models.Model):
#     category = models.CharField(max_length =50,default="python")
#     name = models.CharField(max_length =50)
#     slug = AutoSlugField(populate_from=['name'])
#     hurdle_checkbox = models.BooleanField(default="False")
#     hurdle = RichTextField(blank="True")

#     def __str__(self):
#         return '%s / %s' % (self.category, self.name)




# Create your models here.
class Baseitem(models.Model):
    # homework = models.ForeignKey(Homework, related_name='steps',on_delete=models.CASCADE,)
    itemname = models.CharField(max_length =50)
    # hyperlink = models.CharField(blank = True, max_length =50)
    # content = RichTextField(blank = True)
    # addedon = models.DateTimeField(auto_now_add=True)
    # order = models.DecimalField(max_digits=5, decimal_places=2)
    itemfile = models.CharField(max_length=220, blank=True, null=True)


    class meta :
        ordering = 'id'