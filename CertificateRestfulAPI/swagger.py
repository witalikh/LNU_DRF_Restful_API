from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

SWAGGER_DESCRIPTION = """
Documentation page for describing, visualizing and testing endpoints
"""

schema_view = get_schema_view(
   openapi.Info(
      title="Certificate API",
      default_version='v1',
      description=SWAGGER_DESCRIPTION,
      # terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="vitalii.khomyn@lnu.edu.ua"),
      # license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
