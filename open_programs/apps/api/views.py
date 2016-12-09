from courses.models import Course
from rest_framework import viewsets
from courses.serializers import CourseSerializer


class CourseList(viewsets.ModelViewSet):
    """
    API endpoint that represents a list of users.
    """
    queryset = Course.objects.all().order_by('-created')
    serializer_class = CourseSerializer


# class CourseDetail(viewsets.ModelViewSet):
#     """
#     API endpoint that represents a single user.
#     """
#     model = Course
#     serializer_class = CourseSerializer
