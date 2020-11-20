from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .models import *
import jwt
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework.pagination import PageNumberPagination
from credy.pagination import PaginationHandler
from credy import settings
import requests
from rest_framework.decorators import api_view, renderer_classes
from requests.auth import HTTPBasicAuth
from rest_framework.generics import *
from django.http import HttpResponse

class UsersPagination(PageNumberPagination):
    page_size_query_param = 'user'
    page_size = 10
class CreateUserAPIView(APIView, PaginationHandler):
    # Allow any user (authenticated or not) to access this url
    pagination_class = UsersPagination

    def get_paginator(self):
        page_size = self.request.query_params.get('user')
        if page_size == 'All':
            self.pagination_class.page_size = User.objects.count()

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def get(self,request):
        self.get_paginator()
        users = self.get_queryset()
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_paginated_response((UserSerializer(page,many=True).data))
        else:
            serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                username = serializer.data["username"]
                password = serializer.data["password"]

                user = User.objects.get(username=username, password=password)
                if user:
                    try:
                        payload = jwt_payload_handler(user)
                        token = jwt.encode(payload, settings.SECRET_KEY)
                        user_details = {}
                        user_details['access_token'] = token
                        return Response(user_details, status=status.HTTP_200_OK)

                    except Exception as e:
                        raise e
                else:
                    res = {
                        'error': 'can not authenticate with the given credentials or the account has been deactivated'}
                    return Response(res, status=status.HTTP_403_FORBIDDEN)
            except KeyError:
                res = {'error': 'please provide a username and a password'}
                return Response(res)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def MoviesList(request):
    page=request.GET.get("page")
    if page is None:
        url = requests.get("https://demo.credy.in/api/v1/maya/movies/",
                           auth=HTTPBasicAuth('iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0','Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1'))
    else:
        url = requests.get("https://demo.credy.in/api/v1/maya/movies/?page={}".format(page),auth=HTTPBasicAuth('iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0','Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1'))
    data = url.json()
    return Response(data)

#collection api
class Collections(ListCreateAPIView,UpdateAPIView,DestroyAPIView):
    lookup_field = "collection_uuid"
    serializer_class = Collectionserializer
    queryset = Collection.objects.all()

    def get_queryset(self):
        if self.kwargs["collection_uuid"]:
            data = Collection.objects.filter(
                collection_uuid= self.kwargs["collection_uuid"]
            )
        else:
            data = Collection.objects.all()
        return data

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CollectionGetserializer(queryset, many=True)
        dict = {
            "is_success":True,
            "data": {
                "collections":serializer.data
            }
        }

        return Response(dict)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

#request count api
@api_view(['GET'])
def requestcount(request):
    dic = {
        "requests":request.session['hit']
    }
    return Response(dic)

#sc
class LocalMovies(ListCreateAPIView):
    serializer_class = MoviesSerializer
    queryset = Movies.objects.all()


class feed_data(APIView):
    def get(self, request):
        for i in range(1,4547):
            print(i)
            url = requests.get("https://demo.credy.in/api/v1/maya/movies/?page={}".format(i),
                               auth=HTTPBasicAuth('iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0',
                                                  'Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1'))
            data = url.json()
            serializer = MoviesSerializer(data=data)
            print(serializer)
        if serializer.is_valid():
            serializer.save()
        return Response({"success"})

