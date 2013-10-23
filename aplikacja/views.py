# Create your views here.
#from django.template import Context, loader
#from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext
from zbieracz.models import Wpisy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#import feedparser

#from aplikacja.models import Dribble
#from endless_pagination.views import AjaxListView
#import aplikacja.ajax
#from django.template import RequestContext
#from endless_pagination.decorators import page_template


#@page_template("wpis.html") # just add this decorator
def strona_glowna(request,
    template="index2.html",
    page_template="wpis.html"):

    wpisy_z_db = Wpisy.objects.exclude(img_our_src__isnull=True).exclude(img_our_src__exact='').order_by('-pub_date')

    
    na_ile_podzielic = 25
    if request.is_ajax():
        na_ile_podzielic = 10
    

    paginator = Paginator(wpisy_z_db, na_ile_podzielic)  # Show 25 contacts per page


    page = request.GET.get('page')
    try:
        zpaginowane = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        zpaginowane = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.

        # zpaginowane = paginator.page(paginator.num_pages)
        zpaginowane = []


    Context = {
        'objects': zpaginowane,
        'page_template': page_template,
    }

    if request.is_ajax():
        template = page_template

    return render_to_response(template, Context,
        context_instance=RequestContext(request))

def podstrona(request, id_obrazka, template= "podstrona.html"):
    from django.shortcuts import get_object_or_404
    dane_obrazka = get_object_or_404(Wpisy, pk=id_obrazka)
    # dane_obrazka = Wpisy.objects.get(id=id_obrazka)
    template= "podstrona.html"
    Context = {
        'objects': dane_obrazka,
    }

    if request.is_ajax():
        template = "sam_obrazek.html"

    return render_to_response(template, Context,
        context_instance=RequestContext(request))



# def strona_glowna(request):
#     lista_z_bazy_danych = Dribble.objects.all().order_by('-pub_date')[:5]
#     t = loader.get_template('index.html')
#     c = Context({
#         'lista_z_bazy_danych': lista_z_bazy_danych,
#     })
#     return HttpResponse(t.render(c))




# def strona_glowna(request, template="index.html",
#     extra_context=None):
#     context = {
#         'objects': Dribble.objects.all(),
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#     return render_to_response(template, context,
#         context_instance=RequestContext(request))




# def strona_glowna(request):

# 	caly_feed = feedparser.parse("http://dribbble.com/shots/popular.rss")
# #        feed_test = caly_feed.entries[0]
# #	feed_co =  caly_feed['items'][0]

# 	feed_lista = caly_feed['items']
# 	feed_lista_danych = []
# 	for item in feed_lista:
#         	feed_wpis = unicode(item['summary']).encode("UTF-8")

# 		wpis_tytul = unicode(item['title']).encode("UTF-8")
# 		img_link = unicode(item['link']).encode("UTF-8")
# 		img_data = get_img_data(feed_wpis, '<img', '>', "")
# 		img_alt = get_img_data(img_data, 'alt="', '"', wpis_tytul)
# 		img_src = get_img_data(img_data, 'src="', '"', "")
# 		img_title = get_img_data(img_data, 'title="', '"', wpis_tytul)
# 		feed_lista_danych.append([img_link, img_src, img_alt, img_title])

# 	opis = caly_feed.entries[0].description

# 	return render_to_response('index.html', locals())

# def get_img_data(tekst, przed, za, wartosc_tytulu):
# 	if przed in tekst:
#         	img_cut = tekst.split(przed, 1)[1]
# 		img_cut = img_cut.split(za, 1)[0]
#         	return img_cut
# 	else:
# 		return wartosc_tytulu


# # To podspodem ma zostac w komentarzu


#         feed_lista = caly_feed['items']
#         for numer in feed_lista:
#                 feed_wpis = caly_feed.entries[numer].description
#                 img_link = caly_feed.entries[0].link
#                 img_data = get_img_data(feed_wpis, '<img', '>')
#                 img_alt = get_img_data(img_data, 'alt="', '"')
#                 img_src = get_img_data(img_data, 'src="', '"')
#                 img_title = get_img_data(img_data, 'title="', '"')
