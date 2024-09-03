from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.cache import cache
from jobs.models import BugJob
import json

class Command(BaseCommand):
    help = 'Load job titles and expiry times into Redis'

    def handle(self, *args, **kwargs):
        # Get the underlying Redis client
        redis_client = cache.client.get_client()

        # Clear existing job-related data from Redis
        self.clear_existing_job_data(redis_client)

        # Load all jobs from the database
        jobs = BugJob.objects.all()
        current_time = timezone.now()

        for job in jobs:
            # Convert job_expiry date to datetime by setting the time to midnight (00:00:00)
            job_expiry_datetime = timezone.make_aware(
                timezone.datetime.combine(job.job_expiry, timezone.datetime.min.time()),
                timezone.get_current_timezone()
            )

            # Calculate the expiry time in seconds
            expiry_seconds = int((job_expiry_datetime - current_time).total_seconds())

            if expiry_seconds > 0:
                # Create a dictionary with job details
                job_data = {
                    'id': job.id,
                    'title': job.title.lower(),
                    'job_created': job.job_posted.isoformat(),
                    'job_expiry': job.job_expiry.isoformat(),
                    'salary_min': str(job.salary_min),
                    'salary_max': str(job.salary_max),
                    'job_type': job.job_type,
                    'featured': job.featured
                }

                # Store the job data in Redis with an expiry time
                job_key = f"job:{job.id}"
                redis_client.set(job_key, json.dumps(job_data), ex=expiry_seconds)

                # Add the job title to a Redis set for quick searching
                redis_client.sadd("job_titles", job.title.lower())

        self.stdout.write(self.style.SUCCESS('Successfully loaded job titles and details into Redis'))

    def clear_existing_job_data(self, redis_client):
        try:
            # Find and delete all existing job-related keys
            job_keys = redis_client.keys('job:*')
            if job_keys:
                redis_client.delete(*job_keys)  # Use * to unpack the list of keys for deletion
            # Optionally, delete the job_titles set if it exists
            redis_client.delete('job_titles')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error clearing Redis data: {e}'))
