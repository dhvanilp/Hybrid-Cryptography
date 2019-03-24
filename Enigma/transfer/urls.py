from django.urls import path
from . import views

app_name = 'transfer'

urlpatterns = [
    path('',views.homeView, name="home"),
    path('transfer',views.transferView, name="transfer"),
    path('<name>/send',views.sendView.as_view(), name="send"),
    path('sendFile/<pk>',views.sendFileView, name="sendFile"),

    path('<name>/receive', views.receiveView, name="receive"),
    path('<name>/receiveFile', views.receiveFileView, name="receiveFile"),

    path('decryptFile',views.decryptFile, name="decryptFile"),
    path('downloadFile/<file_name>',views.downloadFile, name="downloadFile"),

    # path('message',views.MessagesView.as_view(), name="messages"),
    # path('generateSOS',views.SOS, name="generateSOS"),
    # path('SOS',views.SOSView.as_view(), name="SOS"),
    # path('SOS/location/<pk>', views.location, name='location'),
    # path('files', views.FilesView.as_view(), name="files"),
    # path('file/<username>',views.FileUploadView.as_view(), name="uploadFile"),
    # path('download/<file_name>', views.downloadFile, name="download"),
    # path('check/<file_name>', views.checkFile, name="check"),
]
