from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from .models import Company, UserProfile


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER

'''Here we are overriding JSONWEBTokenSerializer because we want our users to login with email
and username both also here in response we are adding is_admin so on client side it will be
evaluated if the user is admin or a normal user'''
class CustomJWTSerializer(JSONWebTokenSerializer):          
    username_field = 'email'
    def validate(self, attrs):
        password = attrs.get("password")
        user_obj = User.objects.filter(email=attrs.get("email")).first() or User.objects.filter(username=attrs.get("email")).first()
        if user_obj is not None:
            credentials = {
                'username':user_obj.username,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                print(user)
                if user:
                    if not user.is_active:
                        msg = _('User account is disabled.')
                        raise serializers.ValidationError(msg)
                    payload = jwt_payload_handler(user)
                    return {
                        'token': jwt_encode_handler(payload),
                        'is_admin': user.is_staff,
                        'email': user.email
                    }
                else:
                    msg = _('Unable to log in with provided credentials.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Must include "{username_field}" and "password".')
                msg = msg.format(username_field=self.username_field)
                raise serializers.ValidationError(msg)
        else:
            msg = _('Account with this email/username does not exists')
            raise serializers.ValidationError(msg)


'''This Serializer validating password with build in method validate password.
Also verfying uniqueness of email requested to register. if is_valid() comes true then creating
a user and also an profile for that user. Note:profile model name is UserProfile'''
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, validators=[validate_password])
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
        ]
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

'''This Change passswrod serialzer checking if new passwords are matched
and if not matched then generating validation Error'''
class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

# This serialzer is for the view where admin changing the password of a user without putting old password.
class AdminChangeUserPasswordSerializer(serializers.Serializer):
    model = User
    user_id = serializers.IntegerField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate(self, attrs):
        if not attrs['user_id']:
            raise serializers.ValidationError({'user_id': "company id required."})
        return attrs


# this serialzer getting used in FetchUserProfileSerializer so we can return first and last name of user.
class UpdateUserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    email = serializers.EmailField()
    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'user_id'
        ]


# this serialzer getting used in FetchUserProfileSerializer so we can return first and last name of user.
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
        ]

#This Serializer returning profile to the user and also using UserProfileSerializer
class FetchUserProfileSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'email',
            'profile',
        ]
    def get_profile(self, user):
        profile = UserProfile.objects.filter(user=user).first()
        return UserProfileSerializer(profile).data if profile is not None else None


'''
This Serilizer is a simplest serializer for Company model insuring the field name
so admins set a valueable name for their companies
'''
class CompanyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'name',
        ]

class CompanyUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Company
        fields = [
            'id',
            'name',
        ]
    


'''Serializer to return only id and username fields as needed for frontend'''
class CompaniesFetchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id',
            'name',
        ]


'''
This serializer is recieving user_id and a list of company id's so we can assign
permission to that user for the requested companies.
'''
class CompanyAccessSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    company_list = serializers.ListField(child=serializers.IntegerField(required=True) )
    class Meta:
        model = Company
        fields = [
            'user_id',
            'company_list'
        ]
