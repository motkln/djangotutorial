from rest_framework import serializers
from django.contrib.auth.models import Permission
from .models import User, Role


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"])

        role, created = Role.objects.get_or_create(name="respondents")

        if created:
            role.description = "Respondents can view and answer questions"
            role.save()
            view_question = Permission.objects.get(codename="view_question")
            can_answer = Permission.objects.get(codename="can_answer_question")
            role.permissions.set([view_question, can_answer])

        user.role = role
        user.save()
        return user
