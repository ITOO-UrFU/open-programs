from permission.logics import AuthorPermissionLogic
from permission.logics import CollaboratorsPermissionLogic

PERMISSION_LOGICS = (
    ("courses.Course", AuthorPermissionLogic()),
    ("courses.Course", CollaboratorsPermissionLogic()),
)