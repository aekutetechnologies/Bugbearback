from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.cache import cache
from django.utils import timezone
from .models import BugJob
from .serializers import JobSerializer
import json
from datetime import datetime, date


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.pagination import PageNumberPagination


class JobCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=JobSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                "BugJob Created Successfully", JobSerializer
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                "Invalid input",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        },
    )
    def post(self, request, format=None):
        serializer = JobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = serializer.save()

        # Prepare the job data
        job_data = {
            "id": job.id,
            "title": job.title.lower(),
            "job_created": job.job_posted.isoformat(),
            "job_expiry": job.job_expiry.isoformat(),
            "salary_min": str(job.salary_min),
            "salary_max": str(job.salary_max),
            "job_type": job.job_type,
            "featured": job.featured,
        }

        # Calculate the expiry time in seconds
        current_time = timezone.now()
        expiry_seconds = int((job.job_expiry - current_time).total_seconds())

        if expiry_seconds > 0:
            # Store job in Redis with an expiry time
            job_key = f"job:{job.id}"
            cache.set(job_key, json.dumps(job_data), timeout=expiry_seconds)

            # Store the job title for search purposes
            cache.sadd("job_titles", job.title.lower())

        return Response(
            {"msg": "BugJob Created Successfully", "job": job_data},
            status=status.HTTP_201_CREATED,
        )


class JobPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 100


class JobSearchView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Title to search"
                ),
                "page": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Page number", default=1
                ),
                "page_size": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Number of items per page",
                    default=10,
                ),
                "category": openapi.Schema(
                    type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="List of categories to filter"
                ),
                "salaryRange": openapi.Schema(
                    type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="List of salary ranges"
                ),
                "experienceLevel": openapi.Schema(
                    type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="List of experience levels"
                ),
                "jobType": openapi.Schema(
                    type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="List of job types"
                ),
            },
            required=["page", "page_size"],
        ),
        responses={
            200: openapi.Response(
                "List of jobs",
                openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "title": openapi.Schema(type=openapi.TYPE_STRING),
                            "job_created": openapi.Schema(
                                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
                            ),
                            "job_expiry": openapi.Schema(
                                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
                            ),
                            "salary_min": openapi.Schema(
                                type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT
                            ),
                            "salary_max": openapi.Schema(
                                type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT
                            ),
                            "job_type": openapi.Schema(type=openapi.TYPE_STRING),
                            "featured": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        },
                    ),
                ),
            )
        },
    )
    def post(self, request, format=None):
        # Extracting filter parameters from the request
        search_query = request.data.get("title", "").lower()
        categories = request.data.get("category", [])
        salary_ranges = request.data.get("salaryRange", [])
        experience_levels = request.data.get("experienceLevel", [])
        job_types = request.data.get("jobType", [])

        # Get pagination parameters
        page = request.data.get("page", 1)
        page_size = request.data.get("page_size", 10)

        # Fetch jobs from Redis or database (assuming Redis is used)
        redis_client = cache.client.get_client()
        job_keys = redis_client.keys("job:*")

        # Use a pipeline to batch Redis calls
        pipeline = redis_client.pipeline()
        for job_key in job_keys:
            pipeline.get(job_key)
        job_data_list = pipeline.execute()

        # Initialize matching jobs
        matching_jobs = []

        # Filter through the jobs
        for job_data in job_data_list:
            job_data = json.loads(job_data.decode("utf-8"))
            job_title = job_data.get("title", "").lower()
            job_category = job_data.get("category", "").lower()
            job_salary_min = float(job_data.get("salary_min", 0))
            job_salary_max = float(job_data.get("salary_max", 0))
            job_experience = float(job_data.get("experience", 0))
            job_type_data = job_data.get("job_type", "").lower()

            # Salary filtering logic
            valid_salary = False
            for salary_range in salary_ranges:
                try:
                    min_salary, max_salary = map(float, salary_range.split("-"))
                    if min_salary <= job_salary_min <= max_salary:
                        valid_salary = True
                        break
                except ValueError:
                    valid_salary = False  # Invalid salary range format

            # Check filters
            if (
                (not search_query or search_query in job_title)
                and (not categories or job_category in [cat.lower() for cat in categories])
                and (valid_salary or not salary_ranges)  # If no salary range provided, skip filtering
                and (not experience_levels or any(exp_level.lower() in job_data.get("experience", "").lower() for exp_level in experience_levels))
                and (not job_types or job_type_data in [jt.lower() for jt in job_types])
            ):
                matching_jobs.append(job_data)

        # Sort jobs by job_created
        matching_jobs.sort(key=lambda x: x.get("job_created"), reverse=True)

        # Apply pagination
        paginator = JobPagination()
        paginator.page_size = page_size
        paginated_jobs = paginator.paginate_queryset(matching_jobs, request)

        # Return the paginated response
        return paginator.get_paginated_response(paginated_jobs)




class JobDetailView(APIView):
    # Set default permission classes for all methods
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Override this method to set custom permissions for each HTTP method.
        """
        if self.request.method == "GET":
            # Allow anyone to access the GET method
            return [AllowAny()]
        # Default to IsAuthenticated for all other methods
        return [permission() for permission in self.permission_classes]

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response("Job details", JobSerializer),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                "Job not found",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        }
    )

    def get(self, request, pk, format=None):
        job_key = f"job:{pk}"
        job_data = cache.get(job_key)

        if job_data:
            job_data = json.loads(job_data)
            return Response(job_data, status=status.HTTP_200_OK)

        try:
            job = BugJob.objects.get(pk=pk)
        except BugJob.DoesNotExist:
            return Response(
                {"error": "BugJob not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = JobSerializer(job)

        # Calculate the expiry time in seconds
        current_time = timezone.now()

        # Convert job_expiry to datetime if it's a date
        if isinstance(job.job_expiry, date) and not isinstance(job.job_expiry, datetime):
            job_expiry_datetime = datetime.combine(job.job_expiry, datetime.min.time(), tzinfo=current_time.tzinfo)
        else:
            job_expiry_datetime = job.job_expiry

        expiry_seconds = int((job_expiry_datetime - current_time).total_seconds())

        if expiry_seconds > 0:
            # Save in Redis with the new expiry time
            cache.set(
                f"job:{job.id}", json.dumps(serializer.data), timeout=expiry_seconds
            )

        return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        request_body=JobSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                "Job Updated Successfully", JobSerializer
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                "Job not found",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                "Invalid input",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        },
    )
    def put(self, request, pk, format=None):
        try:
            job = BugJob.objects.get(pk=pk)
        except BugJob.DoesNotExist:
            return Response(
                {"error": "BugJob not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = JobSerializer(job, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Calculate the expiry time in seconds
        current_time = timezone.now()
        expiry_seconds = int((job.job_expiry - current_time).total_seconds())

        if expiry_seconds > 0:
            # Update the job data in Redis
            cache.set(
                f"job:{job.id}", json.dumps(serializer.data), timeout=expiry_seconds
            )

        return Response(
            {"msg": "BugJob Updated Successfully"}, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response("Job Deleted Successfully"),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                "Job not found",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        }
    )
    def delete(self, request, pk, format=None):
        try:
            job = BugJob.objects.get(pk=pk)
        except BugJob.DoesNotExist:
            return Response(
                {"error": "BugJob not found"}, status=status.HTTP_404_NOT_FOUND
            )

        job.delete()

        # Remove job from Redis
        cache.delete(f"job:{pk}")

        return Response(
            {"msg": "BugJob Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT
        )
