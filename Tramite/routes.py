from rest_framework import routers
from django.conf.urls import url,include
from Core.api import resources


router = routers.DefaultRouter()
router.register(r'Office',resources.OfficeViewset,'OfficeViewset')
router.register(r'Tupa',resources.TupaViewset,'TupaViewset')
router.register(r'Type_document',resources.Type_documentViewset,'Type_documentViewset')
router.register(r'Attachments',resources.AttachmentsViewset,'AttachmentsViewset')
router.register(r'Movements',resources.MovementsViewset,'MovementsViewset')
router.register(r'Document_identity',resources.Document_identityViewset,'Document_identityViewset')
router.register(r'Person',resources.PersonViewset,'PersonViewset')
router.register(r'Document',resources.DocumentViewset,'DocumentViewset')


urlpatterns = [
    url(r'^', include(router.urls)),
]
