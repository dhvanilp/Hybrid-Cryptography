from django.views import generic
from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView
from .models import *
from .ECC_module import ECC
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
import ast
from rest_framework.views import APIView

from rest_framework.response import Response
import mimetypes,os
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper




# Create your views here.


def homeView(request):
    return render(request, "transfer/home.html")

def transferView(request):
    name=request.POST['name']
    context={
        'name': name
    }
    return render(request, "transfer/transfer.html", context)

class sendView(CreateView):
    model = File
    fields = ['receiver', 'aes_key', 'file', 'ecc_public']
    sender = ''

    def dispatch(self, request, *args, **kwargs):
        self.sender = self.kwargs['name']
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.sender = self.sender
        if form.is_valid():
            form.save()
            file = File.objects.get(file=form.instance.file)
            file.get_file_type()
            file.encrypt_AES_key()
            file.encrypt_multimedia()
            file.save()
            file_pk=file.pk
            return redirect('transfer:sendFile', file_pk)




def sendFileView(request,pk):
    file=File.objects.get(pk=pk)
    context={
        "file":file
    }
    return render(request, "transfer/home.html", context)


def receiveView(request, name):
    context = {
        'name': name
    }
    return render(request, "transfer/receive.html", context)


def receiveFileView(request, name):
    ecc_private_key=request.POST["ecc_private"]
    ecc_obj_AESkey = ECC.ECC()
    ecc_public_key = ecc_obj_AESkey.gen_pubKey(int(ecc_private_key))
    context={
        "name":name,
        "ecc_private_key": ecc_private_key,
        "ecc_public_key":ecc_public_key
    }
    return render(request, "transfer/receiveFile.html", context)

@csrf_exempt
def decryptFile(request):
    # if the request method is a POST request
    if request.method == 'POST':
        # content sent via XMLHttpRequests can be accessed in request.body
        # and it comes in a JSON string, that's why we use json library to
        # turn it into a normal dictionary again
        msg_obj = json.loads(request.body)

        # tries to create the message and save it in the db
        file_name = msg_obj['file_name'][17:]
        C1_aesKey = ast.literal_eval(msg_obj['C1_aesKey'])
        C2_aesKey = int(msg_obj['C2_aesKey'])
        C1_multimedia = ast.literal_eval(msg_obj['C1_multimedia'])
        C2_multimedia = int(msg_obj['C2_multimedia'])
        private_key = int(msg_obj["ecc_private"])

        ecc_AESkey = ECC.ECC()
        decryptedAESkey = ecc_AESkey.decryption(C1_aesKey, C2_aesKey, private_key)

        ecc_obj = ECC.ECC()
        encrypted_multimedia = ecc_obj.decryption(C1_multimedia, C2_multimedia, private_key)
        clean_data_list = converter.makeListFromString(encrypted_multimedia)

        aes_obj = AES.AES(int(decryptedAESkey))
        decrypted_multimedia = aes_obj.decryptBigData(clean_data_list)


        output_file = "transfer/downloads/" + file_name
        converter.base64ToFile(decrypted_multimedia, output_file)
        data={
            'file_name': file_name
        }

        return HttpResponse(json.dumps({'file_name': file_name}), content_type="application/json")


    else:
        return HttpResponseRedirect('/')


def downloadFile(request,file_name):
    file_path = 'transfer/downloads/'+file_name
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s/' % smart_str(file_name)
    return response