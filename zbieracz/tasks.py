from celery.task.schedules import crontab
from celery.decorators import periodic_task
# from celery.task import PeriodicTask

# this will run every minute, see http://celeryproject.org/docs/reference/celery.task.schedules.html#celery.task.schedules.crontab


# from django.template import RequestContext


@periodic_task(run_every=crontab(hour="*", minute="30", day_of_week="*"))
def zasysamy():
    import feedparser
    import datetime

    from zbieracz.models import RSS
    from zbieracz.models import Wpisy

    print "Shedule RSS"
    RSSy = RSS.objects.all()
    Wszystkie_Wpisy = Wpisy.objects.all()
    lista = [pozycja.rss for pozycja in RSSy]
    for i in lista:
            wpis = RSSy.get(rss=i)
            caly_feed = feedparser.parse(wpis.rss_link)
            print "---------------------------------"
            print str(i) + " RSS: " + wpis.rss_link
            print "---------------------------------"
            feed_lista = caly_feed['items']
            licznik = 0
            for item in feed_lista:
                    licznik = licznik + 1
                    feed_wpis = item['summary']
                    wpis_tytul = item['title']
                    img_link = item['link']
                    if "<img" not in feed_wpis:
                        print ("[ " + str(licznik) + " ] Tytul: [" + wpis_tytul + "]")
                        print ".     Przerywam: Wpis nie posiada obrazka!", "------"
                        continue
                    # def get_img_data(tekst_do_parsowania, przed, za, wartosc_tytulu)
                    img_data = get_img_data(feed_wpis, '<img', '>', "")
                    img_alt = get_img_data(img_data, 'alt="', '"', wpis_tytul)
                    img_src = get_img_data(img_data, 'src="', '"', "")
                    img_title = get_img_data(img_data, 'title="', '"', wpis_tytul)

# Sprawdza czy wpis jest w bazie danych
                    print ("[ " + str(licznik) + " ] Tytul: [" + wpis_tytul + "]")
                    if img_link == None or img_src == None:
                        print ".     Przerywam: Wpis nie posiada obrazka!", "------"
                        continue
                    if Wszystkie_Wpisy.filter(art_link__contains='%s' % img_link):
                        print ".     Przerywam: Wpis jest w bazie danych!", "------"
                        continue

                    bd = Wpisy(rss=wpis, votes=0, art_link=img_link, img_cdn_src=img_src, img_src=img_src, img_alt=img_alt, img_title=img_title, pub_date=datetime.datetime.now())

# Sciaga obrazek z neta
                    nazwa_obrazka, content, result = sciagnij_obrazek(img_src)

                    print ".     nazwa: " + str(nazwa_obrazka)
                    bd.img_our_src.save(nazwa_obrazka, content, save=False)
                    nazwa_obrazka_small = "SMALL_" + nazwa_obrazka

# Zmniejsza obrazek        
                    docelowa_szerokosc = 300
    # Sprawdza czy GIF
                    sciezka_obrazka_tmp = str(content)
                    rozszerzenie_pliku = str(nazwa_obrazka.lower()).rsplit('.', 1)[1] 
                    if rozszerzenie_pliku == "gif":
                        zmniejsz_gifa(sciezka_obrazka_tmp, docelowa_szerokosc)
                    else:
                        zmniejsz_obrazek(sciezka_obrazka_tmp, docelowa_szerokosc)

                    bd.img_our_src_small.save(nazwa_obrazka_small, content, save=False)
                    print ".     " + nazwa_obrazka_small

# Zapisuje wpis do bazy danych
                    try:
                        bd.save()  # zapisuje wpis w bazie danych
                    except Exception, e:
                        print e
                        raise e
                    print "------"
    print "###   KONIEC"


def benchmark(func):
    """
    A decorator that prints the time a function takes
    to execute.
    """
    import time

    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print ".     Wykonano w: " + str(time.clock() - t)
        return res
    return wrapper

#  ----------------------------
#           Funkcje
#  ----------------------------


@benchmark
def sciagnij_obrazek(img_src):
        from django.core.files import File
        import urllib
        from urlparse import urlparse
        nazwa_obrazka = urlparse(img_src).path.split('/')[-1]
        try:
            result = urllib.urlretrieve(img_src)
        except Exception:
            print ".           Nie udalo sie pobrac pliku: " + str(nazwa_obrazka), "------"
        content = File(open(result[0]))

        return nazwa_obrazka, content, result


# Miniaturyzuje obrazek

def zmniejsz_obrazek(sciezka_obrazka_tmp, docelowa_szerokosc):
        import Image
        img = Image.open(open(str(sciezka_obrazka_tmp), 'rb'))
        width, height = img.size
        if width > docelowa_szerokosc:
            aspect_ratio = width / docelowa_szerokosc
            docelowa_wysokosc = int(height / aspect_ratio)
            # if width > (docelowa_szerokosc * 2 + 150):
            #     img.thumbnail((docelowa_szerokosc * 2, docelowa_wysokosc * 2), Image.ANTIALIAS)
            img.thumbnail((docelowa_szerokosc, docelowa_wysokosc), Image.ANTIALIAS)
            width2, height2 = img.size
            try:
                img.save(str(sciezka_obrazka_tmp), quality=90)
                print ".     Zmniejszam: " + str(width) + "x" + str(height) + " >> " + str(width2) + "x" + str(height2)
            except Exception, e:
                raise e
        else:
            img.close()

def zmniejsz_gifa(sciezka_obrazka_tmp, docelowa_szerokosc):
    from subprocess import call
    docelowa_szerokosc = str(docelowa_szerokosc)
    plik = str(sciezka_obrazka_tmp)
    split = str(plik).rsplit('.', 1)
    plik_coalesce =  split[0] + '_COAL.' + split[1]
    print "1 " + str(plik)
    print "2 " + str(plik_coalesce)
    try:
        call('convert -coalesce -quality 10 "' + plik + '" "' + plik_coalesce + '"', shell=True)
        call('convert -resize '+ docelowa_szerokosc + ' -quality 10 "' + plik_coalesce + '" "' + sciezka_obrazka_tmp + '"', shell=True)
        call('rm -f "' + plik_coalesce + '"', shell=True)
    except Exception, e:
        raise e

def get_img_data(tekst, przed, za, wartosc_tytulu):
        if przed in tekst:
                img_cut = tekst.split(przed, 1)[1]
                img_cut = img_cut.split(za, 1)[0]
                return img_cut
        else:
                return wartosc_tytulu
