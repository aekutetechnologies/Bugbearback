from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    SendPasswordResetEmailSerializer,
    UserChangePasswordSerializer,
    UserLoginSerializer,
    UserPasswordResetSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    BugUserDetailSerializer,
    MessageSerializer,
    BugUserEducationSerializer,
    BugBearSkillSerializer,
    BugUserSkillSerializer,
)
from .models import (
    BugUserDetail,
    UserType,
    BugUserEducation,
    BugBearSkill,
    BugUserSkill,
    User
)
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.conf import settings


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={
            201: openapi.Response("Registration Successful", UserRegistrationSerializer)
        },
    )
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

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={200: openapi.Response("Login Success", UserLoginSerializer)},
    )
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")

        user_obj = User.objects.filter(email=email).first()
        if user_obj and user_obj.check_password(password):
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

    @swagger_auto_schema(
        responses={200: openapi.Response("User Profile Details", UserProfileSerializer)}
    )
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=UserChangePasswordSerializer,
        responses={
            200: openapi.Response(
                "Password Changed Successfully", UserChangePasswordSerializer
            )
        },
    )
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

    @swagger_auto_schema(
        request_body=SendPasswordResetEmailSerializer,
        responses={200: openapi.Response("Password Reset Link Sent")},
    )
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Reset link sent. Please check your Email"},
            status=status.HTTP_200_OK,
        )


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    @swagger_auto_schema(
        request_body=UserPasswordResetSerializer,
        responses={
            200: openapi.Response(
                "Password Reset Successfully", UserPasswordResetSerializer
            )
        },
    )
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

    @swagger_auto_schema(
        request_body=BugUserDetailSerializer,
        responses={
            201: openapi.Response("User Details Updated", BugUserDetailSerializer)
        },
    )
    def post(self, request):
        user = request.user
        try:
            bug_user_detail = BugUserDetail.objects.get(user=user)
            serializer = BugUserDetailSerializer(bug_user_detail, data=request.data)
        except BugUserDetail.DoesNotExist:
            serializer = BugUserDetailSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response("User Details", BugUserDetailSerializer)},
    )
    def get(self, request):
        user = request.user
        try:
            bug_user_detail = BugUserDetail.objects.get(user=user)
            serializer = BugUserDetailSerializer(bug_user_detail)
            serializer.data["profile_pic"] = settings.WEB_URL + str(
                bug_user_detail.profile_pic.url
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BugUserDetail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserProfilePic(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"profile_pic": openapi.Schema(type=openapi.TYPE_FILE)},
        ),
        responses={200: openapi.Response("Profile Picture Updated")},
    )
    def post(self, request):
        user = request.user
        if request.FILES.get("profile_pic"):
            try:
                bug_user, _ = BugUserDetail.objects.get_or_create(user=user)
            except BugUserDetail.DoesNotExist:
                return Response(
                    {"error": "User does not have a BugUserDetail object"},
                    status=400,
                )

            profile_pic = request.FILES["profile_pic"]
            bug_user.profile_pic.save(profile_pic.name, profile_pic, save=True)
            profile_pic_url = request.build_absolute_uri(bug_user.profile_pic.url)

            return Response({"profile_pic_path": profile_pic_url}, status=200)
        else:
            return Response({"error": "No profile pic uploaded"}, status=400)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                "Profile Picture URL",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "profile_pic_path": openapi.Schema(type=openapi.TYPE_STRING)
                    },
                ),
            )
        }
    )
    def get(self, request):
        user = request.user
        try:
            bug_user = BugUserDetail.objects.get(user=user)
            profile_pic_url = request.build_absolute_uri(bug_user.profile_pic.url)
            return Response({"profile_pic_path": profile_pic_url}, status=200)
        except BugUserDetail.DoesNotExist:
            return Response(
                {"error": "User does not have a BugUserDetail object"}, status=400
            )


class UserTypes(APIView):
    renderer_classes = [UserRenderer]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                "User Types List",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "user_types": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                                },
                            ),
                        )
                    },
                ),
            )
        }
    )
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


class SendEarlyInvites(APIView):
    renderer_classes = [UserRenderer]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "emails": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                ),
            },
        ),
        responses={200: openapi.Response("Invites Sent")},
    )
    def post(self, request):
        emails = request.data.get("emails")
        if emails:
            for email in emails:
                # Send early invite email
                pass
            return Response({"message": "Invites Sent"}, status=200)
        return Response({"error": "No emails provided"}, status=400)


class UserMessage(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=MessageSerializer,
        responses={200: openapi.Response("Message Sent")},
    )
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Message Sent"}, status=200)
        return Response(serializer.errors, status=400)


class UserEducationView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=BugUserEducationSerializer,
        responses={
            201: openapi.Response("Education Details Added", BugUserEducationSerializer)
        },
    )
    def post(self, request):
        serializer = BugUserEducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                "Education Details List", BugUserEducationSerializer(many=True)
            )
        }
    )
    def get(self, request):
        education_details = BugUserEducation.objects.filter(user=request.user)
        serializer = BugUserEducationSerializer(education_details, many=True)
        return Response(serializer.data, status=200)


class BugBearSkillView(APIView):
    renderer_classes = [UserRenderer]

    @swagger_auto_schema(
        request_body=BugBearSkillSerializer,
        responses={201: openapi.Response("Skill Added", BugBearSkillSerializer)},
    )
    def post(self, request):
        serializer = BugBearSkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        responses={
            200: openapi.Response("Skills List", BugBearSkillSerializer(many=True))
        }
    )
    def get(self, request):
        skills = BugBearSkill.objects.all()
        serializer = BugBearSkillSerializer(skills, many=True)
        return Response(serializer.data, status=200)


class BugUserSkillView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=BugUserSkillSerializer,
        responses={201: openapi.Response("User Skill Added", BugUserSkillSerializer)},
    )
    def post(self, request):
        serializer = BugUserSkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        responses={
            200: openapi.Response("User Skills List", BugUserSkillSerializer(many=True))
        }
    )
    def get(self, request):
        skills = BugUserSkill.objects.filter(user=request.user)
        serializer = BugUserSkillSerializer(skills, many=True)
        return Response(serializer.data, status=200)
