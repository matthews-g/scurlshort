from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView

from urlshortener.models import ShortUrlModel
from urlshortener.serializers import ShortUrlSerializer


class ShortenUrl(APIView):
    """ Shorten a URL. """

    def post(self, request, format=None):

        data = {
            'url': request.data.get('url'),
            'shortcode': ShortUrlModel.generate_short_code(request.data.get('shortcode'))
        }

        # If no url provided...
        if not data['url']:
            return Response({'error': 'Url not present'}, 400)

        # Check if the object already exists...
        try:
            ShortUrlModel.objects.get(shortcode=data['shortcode'])
            return Response({'error': 'Shortcode already in use'}, 409)
        except ObjectDoesNotExist:
            pass

        # Check if the shortcode is satisfying the given rules...
        if not ShortUrlModel.check_shortcode_rules(data['shortcode']):
            return Response({'error': 'The provided shortcode is invalid'}, 412)

        serializer = ShortUrlSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"shortcode": data['shortcode']}, 201)


class GetCodeStats(APIView):
    """ View the statistics of the shortened code """

    def get(self, request, short_code: str, format=None):

        try:
            obj = ShortUrlModel.objects.get(shortcode=short_code)
            serializer = ShortUrlSerializer(obj)
            return Response({"created": serializer.data['creation_date'],
                             "lastRedirect": serializer.data['last_redirect'],
                             "redirectCount": serializer.data['redirect_count']}, 200)
        except ObjectDoesNotExist:
            return Response({'error': 'Shortcode not found'}, 404)


class GetShortCode(APIView):
    """ Make a request with the short code, that will act as the 'redirect' """

    def get(self, request, short_code, format=None):

        try:
            obj = ShortUrlModel.objects.get(shortcode=short_code)
            obj.increment_redirect_count()
            resp = Response({}, 302)
            resp['Location'] = obj.url
            return resp

        except ObjectDoesNotExist:
            return Response({'error': 'Shortcode not found'}, 404)
