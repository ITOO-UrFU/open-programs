from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer, PersonSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Person

User = get_user_model()


@api_view(['POST'])
@permission_classes((AllowAny, ))
def register(request):
    serialized = UserSerializer(data={
        "username": request.data.get("username", None),
        "email": request.data.get("email", None),

    })
    if serialized.is_valid() and request.data['password1'] == request.data['password2'] and request.data['password1']:
        user = User.objects.create_user(
            serialized.validated_data['email'],
            serialized.validated_data['username'],
            request.data['password1']
        )
        print(user, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        person = Person(
            user__id=user.id,
            first_name=request.data.get("first_name", None),
            last_name=request.data.get("last_name", None),
            second_name=request.data.get("second_name", None),
            sex=request.data.get("sex", 'U'),
            alt_email=request.data.get("alt_email", None),
            birthday_date=request.data.get("birthday_date", None),
            biography=request.data.get("biography", ""),
        )
        print(person, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        person.save()

        person = PersonSerializer(person)

        return Response(person, status=201)
    else:
        return Response(serialized._errors, status=400)
