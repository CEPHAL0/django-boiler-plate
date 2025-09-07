from django.core.management.base import BaseCommand
from faker import Faker
from users.models import User

class Command(BaseCommand):
    help = 'Create a set of users'

    def handle(self, *args, **options):
        faker = Faker()

        # Create users
        number_of_users = 10

        for i in range(number_of_users):
            user = User.objects.create_user(
                username = faker.user_name(),
                email = faker.email(),
                password = "#TestUsers123",
                first_name = faker.first_name(),
                last_name = faker.last_name(),
            )
            self.stdout.write(self.style.SUCCESS(f"Created user username: {user.username} email: {user.email}"))

        message = self.style.SUCCESS(f"Successfully created {number_of_users} users")
        self.stdout.write(message)