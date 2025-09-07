# Django Boilerplate

This repository serves as a boilerplate for Django projects, providing a structured setup for handling responses, serializers, views, permissions, logging, and more. It is designed to help developers quickly start a Django project with best practices and reusable components.

---

## Features

### 1. **Custom Response Wrappers**

- Centralized success and error response utilities in [`responses.py`](myapp/utils/responses.py).
- Ensures consistent API responses with fields like `status`, `status_code`, `message`, and `data`.

### 2. **Custom Exception Handling**

- Global exception handler in [`exception_handler.py`](myapp/configurations/exception_handler.py).
- Logs unhandled exceptions and provides user-friendly error messages.

### 3. **Custom Renderers**

- API responses are wrapped in a consistent structure using [`ApiWrapperRenderer`](myapp/configurations/renderers.py).

### 4. **Dynamic Role and Permission Management**

- Management command to dynamically create roles and assign permissions in [`setup_roles.py`](users/management/commands/setup_roles.py).
- Enum-based permission generation in [`application_role_names.py`](myapp/enums/application_role_names.py).

### 5. **Custom User Model**

- Extended `AbstractUser` model with additional fields like `created_at`, `updated_at`, and `deleted_at` in [`models.py`](users/models.py).

### 6. **Swagger Integration**

- Auto-generated API documentation using `drf-yasg`.
- Swagger and ReDoc views available at `/swagger` and `/redoc`.

### 7. **Logging**

- Centralized logging configuration in [`logging.py`](myapp/configurations/logging.py).
- Logs are stored in the `logs/` directory with support for colored console output.

### 8. **Environment Configuration**

- Environment variables are managed using `python-dotenv`.
- Centralized access to environment variables in [`env_constants.py`](myapp/utils/env_constants.py).

### 9. **Custom Base Model**

- Abstract base model with `created_at` and `updated_at` fields in [`base_model.py`](myapp/configurations/base_model.py).

### 10. **Predefined Management Commands**

- `setup_roles`: Dynamically create roles and assign permissions.
- `create_users`: Generate test users using Faker.

---

## Project Structure

### 1. **Clone the Repository**
```bash
git clone https://github.com/your-username/django-boiler-plate.git
cd django-boiler-plate
````

---

### 2. **Set Up Environment Variables**

* Copy the `.env.example` file to `.env`
* Update the `.env` file with your environment-specific values

---

### 3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

---

### 4. **Run Migrations**

```bash
python manage.py migrate
```

---

### 5. **Run the Development Server**

```bash
python manage.py runserver
```

---

### 6. **Access Swagger Documentation**

* Swagger UI: [http://localhost:8000/swagger](http://localhost:8000/swagger)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Management Commands

### 1. **Setup Roles**

Dynamically creates roles and assigns permissions:

```bash
python manage.py setup_roles
```

### 2. **Create Test Users**

Generates 10 test users using Faker:

```bash
python manage.py create_users
```

---

## API Endpoints

### User Endpoints

| Method | Endpoint          | Description                |
| ------ | ----------------- | -------------------------- |
| GET    | `/users/csrf`     | Fetch CSRF token           |
| POST   | `/users/register` | Register a new user        |
| POST   | `/users/login`    | Log in a user              |
| GET    | `/users/logout`   | Log out a user             |
| GET    | `/users/whoami`   | Fetch current user profile |

---

## Dependencies

* Django: **5.2.4**
* Django REST Framework: **3.16.0**
* drf-yasg: **1.21.10**
* Faker: **37.6.0**
* python-dotenv: **1.1.1**
* PostgreSQL: **16** (via Docker)

---

## Docker Setup

### 1. **Build and Run Containers**

```bash
docker-compose up --build
```

### 2. **Access the Application**

* Web: [http://localhost:8000](http://localhost:8000)
* Database: `localhost:5432`
