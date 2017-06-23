from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response

User = get_user_model()


@api_view(['POST'])
def register(request):
    serialized = UserSerializer(data=request.DATA)
    if serialized.is_valid():
        User.objects.create_user(
            serialized.init_data['email'],
            serialized.init_data['username'],
            serialized.init_data['password']
        )

        return Response(serialized.data, status=201)
    else:
        return Response(serialized._errors, status=400)
