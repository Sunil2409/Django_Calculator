# Django Calculator

A simple web-based calculator application built with Django. This project demonstrates basic arithmetic operations through a user-friendly web interface.

## Features

- User authentication (login, signup, logout)
- Basic calculator operations (addition, subtraction, multiplication, division)
- Responsive web interface using Django templates
- Containerized deployment with Docker
- Kubernetes orchestration for scalable deployment

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)
- Virtualenv (recommended for Python environment management)
- Docker (for containerized deployment)
- Kubernetes cluster (e.g., Minikube for local development) and kubectl

## Project Structure

```
calculator/
├── config/                    # Django project configuration
│   ├── Dockerfile            # Docker configuration
│   ├── manage.py             # Django management script
│   ├── requirements.txt      # Python dependencies
│   ├── settings.py           # Django settings
│   └── urls.py               # URL configuration
├── calculator_app/           # Main Django app
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── templates/            # HTML templates
│   └── static/               # Static files (if any)
├── env/                      # Python virtual environment
├── calculator-deploy.yaml    # Kubernetes deployment
├── calculator-pod.yaml       # Kubernetes pod specification
├── calculator-replica.yaml   # Kubernetes replica set
└── calculator-service.yaml   # Kubernetes service
```

## Running the Django Application Locally

1. **Clone or navigate to the project directory:**
   ```
   cd /Users/sunilkumare/Desktop/Code/DJANGO/calculator
   ```

2. **Activate the virtual environment:**
   ```
   source env/bin/activate
   ```

3. **Install dependencies:**
   ```
   pip install -r config/requirements.txt
   ```

4. **Run database migrations (if needed):**
   ```
   cd config
   python manage.py migrate
   ```

5. **Start the Django development server:**
   ```
   python manage.py runserver
   ```

6. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:8000/`

## Running with Docker

1. **Navigate to the config directory:**
   ```
   cd config
   ```

2. **Build the Docker image:**
   ```
   docker build -t django-calculator .
   ```

3. **Run the Docker container:**
   ```
   docker run -p 8000:8000 django-calculator
   ```

4. **Access the application:**
   Open your web browser and go to `http://localhost:8000/`

## Deploying with Kubernetes

1. **Ensure you have a Kubernetes cluster running (e.g., Minikube):**
   ```
   minikube start
   ```

2. **Apply the Kubernetes manifests:**
   ```
   kubectl apply -f calculator-deploy.yaml
   kubectl apply -f calculator-pod.yaml
   kubectl apply -f calculator-replica.yaml
   kubectl apply -f calculator-service.yaml
   ```

3. **Check the deployment status:**
   ```
   kubectl get pods
   kubectl get services
   ```

4. **Access the application:**
   - For Minikube: `minikube service calculator-service`
   - Or get the service IP: `kubectl get service calculator-service`

## Usage

1. Register a new account or login with existing credentials.
2. Use the calculator interface to perform arithmetic operations.
3. Logout when done.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.