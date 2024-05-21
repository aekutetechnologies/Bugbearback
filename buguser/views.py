from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import (
    SendPasswordResetEmailSerializer,
    UserChangePasswordSerializer,
    UserLoginSerializer,
    UserPasswordResetSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    BugUserDetailSerializer,
)
from .models import BugUserDetail, UserType
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .models import User


# Generate Token Manually
def get_tokens_for_user(user):
    print(user)
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user:
            user_profile, _ = BugUserDetail.objects.get_or_create(
                user=user,
                first_name="",
                last_name="",
                country="",
                city="",
                address="",
                phone="",
                profile_pic="",
            )
        token = get_tokens_for_user(user)
        return Response(
            {"token": token, "msg": "Registration Successful"},
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")

        user_obj = User.objects.filter(email=email).first()
        if user_obj.check_password(password):
            token = get_tokens_for_user(user_obj)
            return Response(
                {"token": token, "msg": "Login Success"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"errors": {"non_field_errors": ["Email or Password is not Valid"]}},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        print(request.META.get("HTTP_AUTHORIZATION"))
        print(request.user)
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Changed Successfully"}, status=status.HTTP_200_OK
        )


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Reset link send. Please check your Email"},
            status=status.HTTP_200_OK,
        )


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Reset Successfully"}, status=status.HTTP_200_OK
        )


class UserDetails(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get user from request
        user = request.user

        # Check if BugUserDetail already exists for user
        try:
            bug_user_detail = BugUserDetail.objects.get(user=user)
            serializer = BugUserDetailSerializer(bug_user_detail, data=request.data)
        except BugUserDetail.DoesNotExist:
            serializer = BugUserDetailSerializer(data=request.data)

        # Validate and save serializer
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Get user from request
        user = request.user

        # Check if BugUserDetail already exists for user
        try:
            bug_user_detail = BugUserDetail.objects.get(user=user)
            serializer = BugUserDetailSerializer(bug_user_detail)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BugUserDetail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserProfilePic(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if request.FILES.get("profile_pic"):

            # Get the BugUserDetails object associated with the user_id
            try:
                bug_user, _ = BugUserDetail.objects.get_or_create(user=user)
            except BugUserDetail.DoesNotExist:
                return Response(
                    {"error": "User does not have a BugUserDetail object"},
                    status=400,
                )

            # Save the uploaded profile picture
            profile_pic = request.FILES["profile_pic"]
            bug_user.profile_pic.save(profile_pic.name, profile_pic, save=True)

            # Return the profile pic path in the response
            return Response({"profile_pic_path": bug_user.profile_pic.url}, status=200)
        else:
            return Response({"error": "No profile pic uploaded"}, status=400)

    def get(self, request):
        user = request.user
        try:
            bug_user = BugUserDetail.objects.get(user=user)
            return Response({"profile_pic_path": bug_user.profile_pic.url}, status=200)
        except BugUserDetail.DoesNotExist:
            return Response(
                {"error": "User does not have a BugUserDetail object"}, status=400
            )


class UserTypes(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request):
        user_types = UserType.objects.all()
        return Response(
            {
                "user_types": [
                    {"id": user_type.id, "name": user_type.name}
                    for user_type in user_types
                ]
            },
            status=200,
        )
