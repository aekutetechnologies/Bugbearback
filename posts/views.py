from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import (
    PostSerializer,
    PostCategorySerializer,
    LikePostSerializer,
    CommentSerializer,
)
from .models import Post, PostCategory, Comment
from buguser.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from .models import Post
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

# Create your views here.


class PostListCreateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        posts = Post.objects.filter(user=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostDetailView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this post.")
        return post

    def get(self, request, pk, format=None):
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        """
        Update a post.Verify the user and save the post.
        """
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            post = Post.objects.get(id=pk)
            post.delete()
            return Response(
                {"message": "Delete Successful"}, status=status.HTTP_204_NO_CONTENT
            )
        except Post.DoesNotExist:
            return Response(
                {"message": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND
            )


class PostCreateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListCreateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        categories = PostCategory.objects.all()
        serializer = PostCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfilePostView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        posts = Post.objects.filter(user=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user = request.user
        request.data["user"] = user.id
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk, format=None):
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        post = Post.objects.get(id=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikePostView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, format=None):
        try:
            post = get_object_or_404(Post, id=post_id)

            user = request.user
            if user in post.likes.all():
                post.likes.remove(user)
                message = "Post unliked."
            else:
                post.likes.add(user)
                message = "Post liked."

            post.save()
            return Response(
                {"message": message, "total_likes": post.get_total_likes()},
                status=status.HTTP_200_OK,
            )
        except ValueError:
            raise ValidationError("Invalid post ID provided.")
        except Exception as e:
            raise NotFound("Post not found.") from e


class CommentListView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id, format=None):
        comments = Comment.objects.filter(post=post_id).order_by("-date_added")
        paginator = Paginator(comments, 5)  # Show 5 comments per page

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        serializer = CommentSerializer(page_obj, many=True)
        return Response(serializer.data)

    def post(self, request, post_id, format=None):
        print("here")
        try:
            post = get_object_or_404(Post, id=post_id)
            request.data["post"] = post_id
            request.data["user"] = request.user.id
            serializer = CommentSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            print(post)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except NotFound:
            return Response(
                {"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )


class CommentUpdateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def put(self, request, comment_id, format=None):
        try:
            comment = get_object_or_404(Comment, id=comment_id)
            serializer = CommentSerializer(comment, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound:
            return Response(
                {"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
            )


class CommentLikeView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id, format=None):
        try:
            comment = get_object_or_404(Comment, id=comment_id)
            user = request.user

            if user in comment.likes.all():
                comment.likes.remove(user)
                message = "Comment unliked."
            else:
                comment.likes.add(user)
                message = "Comment liked."

            comment.save()
            return Response({"message": message}, status=status.HTTP_200_OK)
        except NotFound:
            return Response(
                {"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
            )
