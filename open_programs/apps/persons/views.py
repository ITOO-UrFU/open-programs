from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer, PersonSerializer

from django.contrib.auth import authenticate, get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth.models import Group

from .models import Person

from api_v11.views import IsStudent, get_user_by_jwt

User = get_user_model()


@api_view(['POST'])
@permission_classes((AllowAny, ))
def register(request):
    serialized = UserSerializer(data={
        "username": request.data.get("username", None),
        "email": request.data.get("email", None),

    })

    if serialized.is_valid() and request.data['password1'] == request.data['password2'] and request.data['password1']:

        user = User.objects.create_user(serialized.validated_data['username'],
                                        serialized.validated_data['email'],
                                        request.data['password1']
                                        )
        user.is_active = True
        usergroup = Group.objects.get(name="user")
        usergroup.user_set.add(user)
        user.save()

        person = Person.objects.filter(user=user).first()
        if person:
            person.first_name = request.data.get("first_name", "")
            person.last_name = request.data.get("last_name", "")
            person.second_name = request.data.get("second_name", "")
            person.alt_email = request.data.get("alt_email", "")
            person.biography = request.data.get("biography", "")

            person.save()

            person = PersonSerializer(person)

            return Response(person.data, status=201)
    else:
        return Response(serialized.errors, status=400)


class ChangePerson(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = get_user_by_jwt(request)
        person = Person.objects.filter(user=user)

        person.first_name = request.data.get("first_name", "")
        person.last_name = request.data.get("last_name", "")
        person.second_name = request.data.get("second_name", "")
        person.alt_email = request.data.get("alt_email", "")
        person.biography = request.data.get("biography", "")
        person.save()

        person = PersonSerializer(person)

        return Response(person.data, status=201)


class GetUser(APIView):
    permission_classes = (IsStudent, )

    def post(self, request):
        user = get_user_by_jwt(request)
        person = Person.objects.filter(user=user).first()
        person = PersonSerializer(person)
        return Response(person.data, status=201)

change_person = ChangePerson.as_view()
get_user = GetUser.as_view()
