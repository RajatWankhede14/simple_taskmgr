from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from apps.rbac.client import RBACClient

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "mobile", "password", "password_confirm")

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        from apps.core.models import Company
        from django.utils.text import slugify
        
        validated_data.pop("password_confirm")
        username = validated_data["username"]
        
        # Explicit Multi-Tenancy: Create a company for the new Manager
        company = Company.objects.create(
            name=f"{username}'s Company",
            slug=slugify(username)
        )
        
        user = User.objects.create_user(
            username=username,
            email=validated_data.get("email"),
            mobile=validated_data.get("mobile"),
            password=validated_data["password"],
            company=company
        )
        RBACClient().assign_role(user, "MANAGER")
        return user

class ReporteeCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("username", "email", "mobile", "password")

    def create(self, validated_data):
        request = self.context.get("request")
        manager_company = getattr(request.user, "company", None)
        
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            mobile=validated_data.get("mobile"),
            password=validated_data["password"],
            company=manager_company
        )
        RBACClient().assign_role(user, "REPORTEE")
        return user

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "email", "mobile", "role")

    def get_role(self, obj):
        if obj.is_manager:
            return "MANAGER"
        if obj.is_reportee:
            return "REPORTEE"
        return None
