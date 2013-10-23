from dajax.core import Dajax
from dajaxice.core import dajaxice_functions

#@dajaxice_register
def pagination(request, p):
    from projekt.aplikacja.views import get_pagination_page
    from django.template.loader import render_to_string
    try:
        page = int(p)
    except:
        page = 1
    items = get_pagination_page(page)
    render = render_to_string('szablony/pagination.html', { 'objects': items })
    
    dajax = Dajax()
    dajax.assign('#pagination','innerHTML',render)
    return dajax.json()


