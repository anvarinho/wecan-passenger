from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from app.models import Task, Category, Subcategory, User

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class SubcategorySerializer(ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    class Meta:
        model = Subcategory
        fields = ['name', 'category']

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'avatar', 'registered', 'bio', 'name', 'is_master']

class TaskSerializer(ModelSerializer):
    client = UserSerializer(many=False, read_only=True)
    subcategory = SubcategorySerializer(many=False, read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'timesince', 'client', 'subcategory', 'description', 'is_taken', 'is_done', 'price', 'time', 'address']

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=4),
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']

    def validate(self, attrs):
        username = attrs.get('username', '')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'email': ('Email is already in use')})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)
    class Meta:
        model = User
        fields = ['username', 'password']