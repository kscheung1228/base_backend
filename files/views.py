import json
from django.contrib.auth import get_user_model
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.utils.decorators import method_decorator
from .models import S3File
from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response

# from cfehome.aws.utils import AWS
from base_backend.aws.conf import AWS
from .models import S3File
from .serializers import S3FileSerializer

User = get_user_model()

class DownloadView(View):
    def get(self, request, id, *args, **kwargs):
        file_obj = get_object_or_404(S3File, id=id)
        if request.user != file_obj.user:
            raise Http404
        url  = file_obj.get_download_url()
        return HttpResponseRedirect(url)

class UploadView(TemplateView):
    template_name = 'upload.html'


# Django Rest Framework -> REST API course

@method_decorator(csrf_exempt, name='dispatch')
class UploadPolicyView(View): # RESTful API Endpoint
    # def get(self, request, *args, **kwargs):
    #     #key = request.GET.get('key', 'unknown.jpg')
    #     #botocfe = AWS()
    #     #presigned_data = botocfe.presign_post_url(key=key)
    #     return JsonResponse({"detail": "Method not allowed"}, status=403)

    def get(self, request, *args, **kwargs):
        key = request.GET.get('key', 'unknown.jpg')
        botocfe = AWS()
        presigned_data = botocfe.presign_post_url(key=key)
        return JsonResponse(presigned_data)
        

    def put(self, request, *args, **kwargs):
        #print(request.body)
        data = json.loads(request.body)
        key = data.get('key')
        print(key)
        qs = S3File.objects.filter(key=key).update(uploaded=True)
        return JsonResponse({"detail": "Success!"}, status=200)


    # def post(self, request, *args, **kwargs):
    #     """
    #     Requires Security
    #     """
    #     print ("request", request)
    #     # print ("request.body", request.body)
    #     # print(request.body.toString())
    #     print("request.read",request.read())
    #     # body_unicode = request.body.decode('utf-8')
    #     # body_data = json.loads(body_unicode)
    #     # print("body_unicode",body_unicode)
    #     requestread = request.read()
    #     print ("---linebreaker----")
    #     print (requestread)
    #     print ("---linebreaker----")
    #     bodydecode = request.read().decode('cp437')

    #     # print ("request.body.decode('utf-8')",type(request.read().decode('utf-8')))
    #     # print ("body.decode('utf-8')",body.decode('cp437'))
    #     # print("str(body, encoding)",str(body, 'cp437'))

    #     try:
    #         print ("request.names",request.body.names)
    #     except:
    #         pass
        
    #     try:
    #         print ("request.FILES",request.FILES)
    #     except:
    #         pass

    #     try:
    #         print ("request.FILES",request.type)
    #     except:
    #         pass

    #     try:
    #         body_unicode = request.body.decode('utf-8')
    #         body_data = json.loads(body_unicode)
    #         print ("requestbody_unicode")
    #     except:
    #         pass

    #     try:
    #         print(request.META.get('name'))
    #         print(request.META)
    #         print ("requestbodyMETA_name")
    #     except:
    #         pass


    #     try:
    #         print(request.body.get('name'))
    #         print(request.body.get('filename'))
    #         print ("requestbody_name")
    #     except:
    #         pass

    #     try:
    #         print(request.body.toString())
            
    #         print ("requestbody_name.toString")
    #     except:
    #         pass


    #     # print ("request.META",request.META)

        
        
    #     data            = json.loads(request.body)
    #     print ("file serializer post data", data)
    #     filetype = "image/vnd.microsoft.icon"
    #     raw_filename = "IMG_6427.ico"

    #     # files            = json.loads(request.FILES)
    #     serializer      = S3FileSerializer(data=data) # ModelForm
    #     print ("file serializer post data", data)
    #     if serializer.is_valid(raise_exception=True):
    #         validated_data  = serializer.validated_data
    #         raw_filename    = validated_data.pop("raw_filename")
    #         user    = User.objects.first() #cfe user # request.user
    #         qs      = S3File.objects.filter(user=user)
    #         count   = qs.count() + 1
    #         key     = f'users/{user.id}/files/{count}/{raw_filename}'
    #         obj     = serializer.save(
    #                 user=user,
    #                 key=key
    #             )
    #         botocfe = AWS()
    #         presigned_data = botocfe.presign_post_url(key=key)
    #         presigned_data['object_id'] = obj.id

    #         return JsonResponse(presigned_data)
    #     return JsonResponse({"detail": "Invalid request"}, status=401)

    def post(self, request, *args, **kwargs):
        """
        Requires Security
        """
        print ("type(request.FILES)",type(request.FILES.getlist('file')))
        print ("type(request.FILES)",request.FILES.getlist('file'))

        # print ("type(request.FILES)",type(request.FILES['file']))
        # print ("type(request.FILES)",request.FILES['file'])
    
        filetype = "image/vnd.microsoft.icon"
        raw_filename = "IMG_6427.ico"
        user    = User.objects.first() #cfe user # request.user
        qs      = S3File.objects.filter(user=user)
        count   = qs.count() + 1
        key     = f'users/{user.id}/files/{count}/{raw_filename}'
        # obj     = serializer.save(
        #         user=user,
        #         key=key
        #     )
        botocfe = AWS()
        presigned_data = botocfe.presign_post_url(key=key)
        # presigned_data['object_id'] = obj.id
        # uploadedfile_data = botocfe.upload_file(fileobj=request.FILES, key=key)
        # print ("uploadedfile_data",uploadedfile_data)
        return JsonResponse(presigned_data)



class S3FileViewSet(viewsets.ModelViewSet):
    queryset = S3File.objects.all()
    serializer_class = S3FileSerializer

    def list (self,request, *arg, **kwargs):
        s3files = S3File.objects.all()
        serializer = S3FileSerializer(s3files, many = True)
        return Response(serializer.data)


   