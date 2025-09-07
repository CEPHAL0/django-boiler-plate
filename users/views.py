from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.views import APIView

from myapp.configurations.yasg_wrapper import make_response_serializer, swagger_response
from myapp.utils.responses import success, error
from myapp.permissions.core_roles import IsSuperAdmin
from tenants.models import TenantRoleGroup, Tenant
from users.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout as a_logout, authenticate
from myapp.configurations.logging import logger
from rest_framework import serializers


class GetCsrfToken(APIView):
    """
    Set the CSRF Token as a cookie on response
    """

    @swagger_response(
        input_serializer=None,
        output_serializer=None,
        responses={
            status.HTTP_200_OK: {
                "desc": "Successfully Set the CSRF Token",
                "message": "CSRF token set",
            }
        },
    )
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        logger.info("Setting CSRF Token")
        return success("CSRF token set", {}, status.HTTP_200_OK)


class RegisterUserView(APIView):
    class InputSerializer(serializers.ModelSerializer):
        first_name = serializers.CharField(required=True)
        last_name = serializers.CharField(required=True)

        class Meta:
            ref_name = "RegisterUserInput"
            model = User
            fields = ["username", "email", "password", "first_name", "last_name"]

        def create(self, validated_data):
            logger.info(validated_data)
            return User.objects.create_user(**validated_data)

    class OutputSerializer(serializers.Serializer):
        class Meta:
            ref_name = "RegisterUserOutput"
            model = User
            fields = [
                "username",
                "email",
                "first_name",
                "last_name",
                "created_at",
                "updated_at",
            ]

    @swagger_response(
        input_serializer=InputSerializer,
        output_serializer=OutputSerializer,
        responses={
            status.HTTP_200_OK: {
                "detail": "Successful Register",
                "message": "User Created Successfully",
            }
        },
    )
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return success("User created successfully", self.OutputSerializer(user).data)


class LoginUserView(APIView):
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField(required=True)
        password = serializers.CharField(required=True)

        class Meta:
            ref_name = "LoginUserInput"

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        username = serializers.CharField()
        email = serializers.EmailField()

        class Meta:
            ref_name = "LoginUserOutput"

    @swagger_response(
        input_serializer=InputSerializer,
        output_serializer=OutputSerializer,
        responses={
            status.HTTP_200_OK: {
                "detail": "Successful Login",
                "message": "User Logged In Successfully",
            },
            status.HTTP_404_NOT_FOUND: {
                "detail": "Invalid Credentials",
                "message": "Invalid Credentials",
            },
        },
    )
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        user = User.objects.filter(username=username).first()

        if not user:
            return error("User not found", {}, status.HTTP_404_NOT_FOUND)

        logged_user = authenticate(request, user=user)
        if not logged_user:
            return error("Invalid Credentials", {}, status.HTTP_404_NOT_FOUND)

        login(request, user)
        logger.info(f"Logged in {user.username}")

        return success("User logged in successfully", self.OutputSerializer(user).data)


class LogoutUserView(APIView):
    @swagger_response(
        input_serializer=None,
        output_serializer=None,
        responses={
            status.HTTP_200_OK: {
                "detail": "Successful Logout",
                "message": "User logged out",
            }
        },
    )
    def get(self, request):
        a_logout(request)
        logger.info(f"Logged out {request.user.username}")
        return success("User logged out successfully", {}, HTTP_200_OK)


class WhoAmIView(APIView):
    class OutputPermissionSerializer(serializers.ModelSerializer):
        class Meta:
            model = Permission
            fields = ["id", "name", "codename"]

    class OutputTenantSerializer(serializers.ModelSerializer):
        class Meta:
            ref_name = "WhoAmITenantOutput"
            model = Tenant
            fields = "__all__"

    class OutputRoleGroupSerializer(serializers.ModelSerializer):
        permissions = serializers.SerializerMethodField()
        tenant = serializers.SerializerMethodField()

        class Meta:
            model = TenantRoleGroup
            fields = ["id", "name", "tenant", "permissions", "created_at", "updated_at"]

        def get_permissions(self, obj):
            permissions = [trp.permission for trp in obj.tenant_role_permissions.all()]
            return WhoAmIView.OutputPermissionSerializer(permissions, many=True).data

        def get_tenant(self, obj):
            tenant = obj.tenant
            return WhoAmIView.OutputTenantSerializer(tenant).data

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                "id",
                "username",
                "email",
                "first_name",
                "last_name",
                "is_superuser",
                "is_active",
            ]

    @swagger_response(
        input_serializer={"username": "string", "password": "string"},  # dict example
        output_serializer={
            "user": OutputSerializer,
            "role_group": OutputRoleGroupSerializer,
        },  # dict of serializers
        responses={
            200: {
                "desc": "Profile fetched",
                "message": "Profile Fetched Successfully",
                "example": {
                    "user": {"id": 1, "username": "demo"},
                    "role_group": {"id": 10, "name": "Admin"},
                },
            },
            400: {
                "desc": "Unauthenticated",
                "message": "User not authenticated",
                "example": {},
            },
        },
    )
    def get(self, request):
        if not request.user.is_authenticated:
            return error("User not authenticated", status=HTTP_400_BAD_REQUEST)

        user = (
            User.objects.filter(id=request.user.id)
            .prefetch_related("tenant_role_group_user__tenant_role_group")
            .first()
        )

        role_group = user.role_group

        data = {
            "user": self.OutputSerializer(user).data,
            "role_group": self.OutputRoleGroupSerializer(role_group).data,
        }
        return success("Profile Fetched Successfully", data)


# Create your views here.
class FetchAllUsers(APIView):
    permission_classes = [IsSuperAdmin]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                "id",
                "username",
                "email",
                "first_name",
                "last_name",
                "created_at",
                "updated_at",
            ]

    def get(self, request):
        users = User.objects.all()
        serializer = self.OutputSerializer(users, many=True)
        return success("Fetched All Users", payload=serializer.data)
