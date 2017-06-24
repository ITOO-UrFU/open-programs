from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer, PersonSerializer

from django.contrib.auth import authenticate, get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Person

User = get_user_model()


@receiver(post_save, sender=User)
def create_favorites(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def register(request):
    serialized = UserSerializer(data={
        "username": request.data.get("username", None),
        "email": request.data.get("email", None),

    })
    if serialized.is_valid() and request.data['password1'] == request.data['password2'] and request.data['password1']:
        user = User(
            email=serialized.validated_data['email'],
            username=serialized.validated_data['username'],
            password=request.data['password1']
        )
        user.save()

        person = Person.objects.filter(user=user).first()
        if person:
            person.first_name = request.data.get("first_name", ""),
            person.last_name = request.data.get("last_name", ""),
            person.second_name = request.data.get("second_name", ""),
            person.sex = request.data.get("sex", 'U'),
            person.alt_email = request.data.get("alt_email", ""),
            person.birthday_date = request.data.get("birthday_date", None),
            person.biography = request.data.get("biography", ""),

            person.save()

            person = PersonSerializer(person)

            return Response(person, status=201)
    else:
        return Response(serialized._errors, status=400)
