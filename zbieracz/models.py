from django.db import models
# from django.core.files import File
# import urllib
# Create your models here.
# import os
# from random import randint
from time import gmtime, strftime

import datetime
from django.utils import timezone

# from core import tasks


def benchmark(func):
    """
    A decorator that prints the time a function takes
    to execute.
    """
    import time

    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print ".      Wykonano w: " + str(time.clock() - t)
        return res
    return wrapper


def logging(func):
    """
    A decorator that logs the activity of the script.
    (it actually just prints it, but it could be logging!)
    """
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print ".      ", func.__name__, args, kwargs
        return res
    return wrapper


def counter(func):
    """
    A decorator that counts and prints the number of times a function has been executed
    """
    def wrapper(*args, **kwargs):
        wrapper.count = wrapper.count + 1
        res = func(*args, **kwargs)
        print "{0} has been used: {1}x".format(func.__name__, wrapper.count)
        return res
    wrapper.count = 0
    return wrapper


# class AvatarImageField(models.ImageField):
#     print "jestem tuuu"

#     def save_from_data(self, instance, data):
#         from StringIO import StringIO
#         from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
#         import settings
#         print "jestem tu"
#         if data and isinstance(data, UploadedFile):
#             print "jestem tam"
#             image = imageResize(data)
#             new_image = StringIO()
#             image.save(new_image, quality=100)
#             data = SimpleUploadedFile(data.name, new_image.getvalue(), data.content_type)

#             previous = u'%s%s' % (settings.MEDIA_ROOT, instance.avatar)
#             if os.path.isfile(previous):
#                 os.remove(previous)
#         super(AvatarImageField, self).save_form_data(instance, data)


# def imageResize(data):
#     img = Image.open(data)
#     docelowa_szerokosc = 200
#     width, height = img.size
#     if width > docelowa_szerokosc:
#         aspect_ratio = width / docelowa_szerokosc
#         docelowa_wysokosc = int(height / aspect_ratio)
#         # if width > (docelowa_szerokosc * 2 + 150):
#             # img.thumbnail((docelowa_szerokosc * 2, docelowa_wysokosc * 2), Image.ANTIALIAS)
#         img = img.thumbnail((docelowa_szerokosc, docelowa_wysokosc), Image.ANTIALIAS)
#         width2, height2 = img.size
#         print ".        Miniaturyzacja: " + str(width) + "x" + str(height) + " >> " + str(width2) + "x" + str(height2)
#         return img
#     else:
#         return img

# -----------------------------------
# .       Modele bazy danych        .
# -----------------------------------


class RSS(models.Model):
    rss = models.AutoField(primary_key=True)
    rss_name = models.CharField(max_length=100)
    rss_link = models.URLField(max_length=300)

    class Meta:
        verbose_name = "RSS"
        verbose_name_plural = "RSSy"

    def __unicode__(self):
                return self.rss_name


class Wpisy(models.Model):
    def upload_path(self, filename):
        splited = str(self.rss_id).split('_', 1)[0]  # 1_12 rozdziela na same 1
        filename = splited + '_' + filename  # 1_costam.jpg
        return "%s/%s/%s" % (splited, strftime('%Y/%m', gmtime()), filename)  # 1/2012/10/plik.jpg

    def upload_path_small(self, filename):
        splited = str(self.rss_id).split('_', 1)[0]  # 1_12 rozdziela na same 1
        filename = splited + "_" + filename  # 1_small_costam.jpg
        return "%s/%s/%s" % (splited, strftime('%Y/%m', gmtime()), filename)  # 1/2012/10/plik.jpg

    rss = models.ForeignKey(RSS)
    pub_date = models.DateTimeField('date published')
    votes = models.IntegerField()
    art_link = models.CharField(max_length=300)
    img_our_src = models.ImageField(upload_to=upload_path, blank=True)
    img_our_src_small = models.ImageField(upload_to=upload_path_small, blank=True)
    img_cdn_src = models.URLField(max_length=300)
    # img_cdn_src_small = models.ImageField(upload_to=upload_path_small, blank=True)
    img_src = models.URLField(max_length=255, unique=True)
    img_alt = models.CharField(max_length=100)
    img_title = models.CharField(max_length=100)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Today?'

    class Meta:
        verbose_name = "Wpis"
        verbose_name_plural = "Wpisy"

    # @benchmark
    # def Miniaturyzacja(self):
    #     # if self.img_src and not self.img_our_src:
    #         print "super partia"
    #         try:
    #             result = urllib.urlretrieve(self.img_our_src.path)
    #             print "asd"
    #             print urllib.urlretrieve(self.img_our_src.path)
    #             print "sdf"
    #             # print File(open(self.img_our_src))
    #             print self.img_our_src
    #             print "dfg"
    #             self.img_our_src_small.save("/asd.jpg", self.img_our_src, save=False)
    #             print "SUCCCCCCESSSS"
    #         except Exception, e:
    #             print e
    #             raise e
    #         self.save()
    #         print "costam"
    #         docelowa_szerokosc = 250
    #         img = Image.open(self.img_our_src_small)
    #         width, height = img.size
    #         if width > docelowa_szerokosc:
    #             aspect_ratio = width / docelowa_szerokosc
    #             docelowa_wysokosc = int(height / aspect_ratio)
    #             # if width > (docelowa_szerokosc * 2 + 150):
    #                 # img.thumbnail((docelowa_szerokosc * 2, docelowa_wysokosc * 2), Image.ANTIALIAS)
    #             img.thumbnail((docelowa_szerokosc, docelowa_wysokosc), Image.ANTIALIAS)
    #             width2, height2 = img.size
    #             try:
    #                 img.save(file(str(self.img_our_src_small), "w"), quality=100)
    #                 print ".        Miniaturyzacja: " + str(width) + "x" + str(height) + " >> " + str(width2) + "x" + str(height2)
    #             except Exception, e:
    #                 raise e
    #         else:
    #             img.close()

    # def __unicode__(self):
    #         return self.img_title


    # @benchmark
    # def cache(self):
    #     # if self.img_src and not self.img_our_src:
    #         result = urllib.urlretrieve(self.img_src)
    #         print ".        Sciagniety: " + os.path.basename(self.img_src)
    #         try:
    #             self.img_our_src.save(os.path.basename(self.img_src), File(open(result[0])))
    #         except Exception, e:
    #             print e
    #             raise e
    #         self.save()
    #         docelowa_szerokosc = 250
    #         img = Image.open(self.img_our_src)
    #         width, height = img.size
    #         if width > docelowa_szerokosc:
    #             aspect_ratio = width / docelowa_szerokosc
    #             docelowa_wysokosc = int(height / aspect_ratio)
    #             # if width > (docelowa_szerokosc * 2 + 150):
    #                 # img.thumbnail((docelowa_szerokosc * 2, docelowa_wysokosc * 2), Image.ANTIALIAS)
    #             img.thumbnail((docelowa_szerokosc, docelowa_wysokosc), Image.ANTIALIAS)
    #             width2, height2 = img.size
    #             try:
    #                 img.save(file(str(self.img_our_src), "w"), quality=100)
    #                 print ".        Miniaturyzacja: " + str(width) + "x" + str(height) + " >> " + str(width2) + "x" + str(height2)
    #             except Exception, e:
    #                 raise e
    #         else:
    #             img.close()

                # pliczek = Image(open(result[0]))
                # pliczek.thumbnail((400,400))
                # pliczek.thumbnail((200,200), Image.ANTIALIAS)




# -------------------------------------
# .              Funkcje              .
# -------------------------------------
