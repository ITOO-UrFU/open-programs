from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

User = get_user_model()


@api_view(['POST'])
@permission_classes((AllowAny, ))
def register(request):
    serialized = UserSerializer(data={
        "username": request.data.get("username", None),
        "email": request.data.get("email", None),
        "password": request.data.get("password1", None),

    })
    if serialized.is_valid():
        User.objects.create_user(
            serialized.init_data['email'],
            serialized.init_data['username'],
            serialized.init_data['password']
        )

        return Response(serialized.data, status=201)
    else:
        return Response(serialized._errors, status=400)
