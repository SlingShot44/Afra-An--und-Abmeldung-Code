from .models import Tour, Account
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import TourSerializer
from rest_framework.exceptions import ValidationError
from dateutil import parser
from datetime import timezone
from rest_framework.renderers import JSONRenderer
from .json_tools import house_dict, house_list
from WebApp.utils import printPDF
from django.http import HttpRequest

# Create your views here.

#Client
@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def function_view(request: HttpRequest, uid: int) -> Response:
    if not Account.objects.filter(uid=uid).exists():
        return Response({"detail":f"Account with uid {uid} doesn't exist."}, status=status.HTTP_404_NOT_FOUND)
    owner = Account.objects.get(uid=uid)
    if Tour.objects.filter(owner=owner, back=False).exists():
        tour = Tour.objects.get(owner=owner, back=False)
        if request.method == 'POST':
            serializer = TourSerializer(tour)
            return Response(serializer.data, status=status.HTTP_409_CONFLICT)

        if request.method == 'DELETE':
            serializer = TourSerializer(tour, data={'target': tour.target, 'end': tour.end})
            if not serializer.is_valid():
                raise ValidationError(serializer.errors)
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.method == 'GET':
            serializer = TourSerializer(tour)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    else:
        if request.method == 'POST':
            if Account.objects.filter(uid=uid).exists():
                ind_str = request.data.get("target", "pi")
                try: 
                    ind_int = int(ind_str)
                except ValueError:
                    ind_int = "pi"
                if ind_int == "pi" or ind_int < 0 or (len(house_list()) - 1) < ind_int:
                    length = (len(house_list()) - 1) if len(house_list()()) > 0 else 0 
                    return Response({"detail": f"'target' needs to be an integer value in the interval [0;{length}]"}, status=status.HTTP_400_BAD_REQUEST)
                target_str = house_list()[ind_int] if house_dict[house_list()[ind_int]] else None
                if target_str is None:
                    return Response({"detail":f"The target '{ind_int}'({house_list()[ind_int]}) is deactivated. Choose another one."}, status=status.HTTP_400_BAD_REQUEST)
                serializer = TourSerializer(data={'target': ind_int, 'end': parser.parse(request.data['end']).astimezone(timezone.utc)}, context={'uid': uid})
                if not serializer.is_valid():
                    raise ValidationError(serializer.errors)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"detail": f"There's no account with the uid '{uid}'."}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            return Response({"detail": "There's nothing to delete with this uid."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            return Response({"detail": f"There's no account with the uid '{uid}', that's away right now."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer])
def option_view(request: HttpRequest) -> Response:
    return Response(house_dict(), status=status.HTTP_200_OK)

@api_view(['GET'])
def tour_list(request: HttpRequest) -> Response:
    tours = Tour.objects.all()
    serializer = TourSerializer(tours, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def print_view(request: HttpRequest) -> Response:
    printPDF()
    return Response({"detail":"Printing..."}, status=status.HTTP_200_OK)

