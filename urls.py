"""File for linking routes between http queries and django views."""

from django.conf.urls import (
    url, include, handler400, handler403, handler404, handler500
)
from django.views.decorators.csrf import csrf_exempt

from backend import services
from backend.api.schema import SCHEMA
from backend.api.view import APIView
from backend.decorators import verify_csrf
try:
    import ariadne  # noqa
    NEW_API = True
except ImportError:
    NEW_API = False

from app import views

# pylint: disable=pointless-statement
handler400, handler403, handler404, handler500, handler501

# pylint: disable=invalid-name
handler400 = 'app.views.error401'
handler401 = 'app.views.error401'
handler403 = 'app.views.error401'
handler404 = 'app.views.error401'
handler500 = 'app.views.error500'
handler501 = 'app.views.error501'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Principal process.
    url(r'^/?index/?$', views.index, name='index'),
    url(r'^/?error500/?$', views.error500, name='error500'),
    url(r'^/?error401/?$', views.error401, name='error401'),
    url(r'^/?login/?$', services.login, name='login'),
    url(r'^/?logout/?$', views.logout, name='logout'),
    url(r'^/?dashboard/?$', views.app, name='dashboard'),
    url(r'^/?registration/?$', views.app, name='registration'),
    url(r'^/?oauth/', include('social_django.urls', namespace='social')),
    url(r'^/?api/?\.*$',
        csrf_exempt(verify_csrf(APIView.as_view(schema=SCHEMA)))),
    # Use of Formstack services.
    url(r'^/?project/(?P<project>[A-Za-z0-9]+)/(?P<evidence_type>[A-Za-z0-9]+)/'
        r'(?P<findingid>[0-9]+)/([A-Za-z.=]+)/(?P<fileid>[\w\.-]+)?$',
        views.get_evidence),
    url(r'^/?(?P<findingid>[0-9]+)/download_vulnerabilities?$',
        views.download_vulnerabilities),
    # Documentation.
    url(r'^/?pdf/(?P<lang>[a-z]{2})/project/(?P<project>[A-Za-z0-9]+)/(?P<doctype>[a-z]+)/?$',
        views.project_to_pdf),
    url(r'^/?xls/(?P<lang>[a-z]{2})/project/(?P<project>[A-Za-z0-9]+)/?$',
        views.project_to_xls),
    url(r'^/?complete_report/?$', views.generate_complete_report),
    url(r'^/?export_all_vulnerabilities/?$', views.export_all_vulnerabilities),
    url(r'^/?export_users/?$', views.export_users)
]

if NEW_API:
    urlpatterns.append(
        url(r'^/?v2/?\.*$',
            csrf_exempt(verify_csrf(APIView.as_view(schema=SCHEMA)))),
    )
