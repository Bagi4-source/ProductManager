import requests
from rest_framework import viewsets, mixins
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from Dewu.settings import API_URL
from .models import Products
from . import serializers
from django.http import JsonResponse


class ProductsView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProductsSerializer
    queryset = Products.objects.all()

    def get_queryset(self):
        brand = self.request.GET.get('brand', None)
        spu = self.request.GET.get('spu_id', None)
        if spu:
            return Products.objects.filter(spu_id=spu)
        if brand:
            return Products.objects.filter(brand=brand)
        return Products.objects.all()


def parse_products(spu_ids: list):
    url = f"{API_URL}getOffers/"
    params = {
        "spuIds": spu_ids
    }
    result = requests.post(url, json=params)
    if result.ok:
        return result.json()
    return []


class GetProductsView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = min(max(int(request.GET.get('limit', 50)), 1), 100)
        offset = max(int(request.GET.get('offset', 0)), 0)

        productsSet = Products.objects.all()
        count = productsSet.count()
        productsSet = productsSet[offset:offset + limit]
        spu_ids = []
        products = {}

        for product in productsSet.values():
            spu_ids.append(product.get('spu_id'))
            products[product.get('spu_id')] = {
                'title': product.get('override_title'),
                'brand': product.get('override_brand')
            }

        parsed_products = parse_products(spu_ids)

        for product in parsed_products:
            cur_product = products.get(product.get('spuId', ''))
            if cur_product:
                if cur_product.get('brand'):
                    product['brand'] = cur_product.get('brand')
                if cur_product.get('title'):
                    product['title'] = cur_product.get('title')

        nextUrl = None
        prevUrl = None
        protocol = 'https' if request.is_secure() else 'http'

        if count > offset + limit:
            nextUrl = f'{protocol}://{request.get_host()}{request.path}?limit={limit}&offset={offset + limit}'
        if offset >= limit:
            prevUrl = f'{protocol}://{request.get_host()}{request.path}?limit={limit}&offset={offset - limit}'

        result = {
            'count': len(parsed_products),
            'next': nextUrl,
            'prev': prevUrl,
            'products': parsed_products
        }

        return JsonResponse(result)

#
# class RequestView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
#     permission_classes = [AllowAny]
#     serializer_class = serializers.RequestSerializer
#     queryset = Request.objects.all()
#     ordering_fields = ['pk']
#     filter_backends = [filters.OrderingFilter]
#
#     def get_queryset(self):
#         telegram_id = self.request.GET.get('telegram_id', None)
#         if telegram_id:
#             return Request.objects.filter(telegram_id=telegram_id)
#         else:
#             return Request.objects.all()
#
#
# class ResultsView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
#     permission_classes = [AllowAny]
#     serializer_class = serializers.ResultsSerializer
#     queryset = Results.objects.all()
#     ordering_fields = ['pk']
#     filter_backends = [filters.OrderingFilter]
#
#     def get_queryset(self):
#         telegram_id = self.request.GET.get('telegram_id', None)
#         if telegram_id:
#             return Results.objects.filter(telegram_id=telegram_id)
#         else:
#             return Results.objects.all()
#
#
# class AdminRequestView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
#                        mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
#     permission_classes = [AllowAny]
#     serializer_class = serializers.RequestSerializer
#     queryset = Request.objects.filter(status=False, viewed=False)
#
#
# class MessagesView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
#                    mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
#     permission_classes = [AllowAny]
#     serializer_class = serializers.MessagesSerializer
#     queryset = Messages.objects.all()
#
#     def get_queryset(self):
#         tag = self.request.GET.get('tag', None)
#         if tag:
#             return Messages.objects.filter(tag=tag)
#         else:
#             return Messages.objects.all()
#
#
# class TariffView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
#                  mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
#     permission_classes = [AllowAny]
#     serializer_class = serializers.TariffSerializer
#     queryset = Tariff.objects.all()
#     ordering_fields = ['days']
#     filter_backends = [filters.OrderingFilter]
#
#
# @receiver(pre_save, sender=Request)
# def my_callback(sender, instance, *args, **kwargs):
#     current_request = Request.objects.filter(pk=instance.pk)
#     if current_request:
#         current_request = current_request.first()
#         if current_request.telegram_id != instance.telegram_id:
#             raise Exception('Changing telegram_id')
#         if current_request.amount != instance.amount:
#             raise Exception('Changing amount')
#         if current_request.tariff != instance.tariff:
#             raise Exception('Changing tariff')
#         if not current_request.status and instance.status:
#             user = User.objects.get(telegram_id=instance.telegram_id)
#             if user:
#                 user.subscription_end = max(user.subscription_end, datetime.today().date()) + timedelta(
#                     days=instance.tariff)
#                 user.save()
