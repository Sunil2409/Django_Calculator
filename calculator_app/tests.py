"""
Comprehensive test suite for the calculator application.

Covers: arithmetic operations, authentication flows, calculator views,
calculation history persistence, and health-check endpoint.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .operations import add, subtract, multiply, divide, DivisionByZeroError
from .models import CalculationHistory


# ─── Unit Tests: Arithmetic Operations ───────────────────────────────────────


class AdditionTest(TestCase):
    """Tests for the add() function."""

    def test_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_negative_numbers(self):
        self.assertEqual(add(-1, -1), -2)

    def test_mixed_sign(self):
        self.assertEqual(add(-5, 10), 5)

    def test_floats(self):
        self.assertAlmostEqual(add(0.1, 0.2), 0.3, places=10)

    def test_zeros(self):
        self.assertEqual(add(0, 0), 0)


class SubtractionTest(TestCase):
    """Tests for the subtract() function."""

    def test_positive_numbers(self):
        self.assertEqual(subtract(10, 4), 6)

    def test_negative_result(self):
        self.assertEqual(subtract(3, 7), -4)

    def test_same_numbers(self):
        self.assertEqual(subtract(5, 5), 0)


class MultiplicationTest(TestCase):
    """Tests for the multiply() function."""

    def test_positive_numbers(self):
        self.assertEqual(multiply(3, 7), 21)

    def test_by_zero(self):
        self.assertEqual(multiply(5, 0), 0)

    def test_negative_numbers(self):
        self.assertEqual(multiply(-2, -3), 6)

    def test_mixed_sign(self):
        self.assertEqual(multiply(-4, 5), -20)


class DivisionTest(TestCase):
    """Tests for the divide() function."""

    def test_exact_division(self):
        self.assertEqual(divide(10, 2), 5)

    def test_float_result(self):
        self.assertAlmostEqual(divide(1, 3), 0.3333, places=3)

    def test_divide_by_zero_raises(self):
        with self.assertRaises(DivisionByZeroError):
            divide(1, 0)

    def test_negative_division(self):
        self.assertEqual(divide(-10, 2), -5)


# ─── Integration Tests: Health Check ─────────────────────────────────────────


class HealthCheckTest(TestCase):
    """Tests for the /health/ endpoint."""

    def test_returns_200(self):
        response = self.client.get(reverse("health_check"))
        self.assertEqual(response.status_code, 200)

    def test_returns_json(self):
        response = self.client.get(reverse("health_check"))
        self.assertEqual(response.json(), {"status": "healthy"})


# ─── Integration Tests: Authentication ───────────────────────────────────────


class AuthenticationTest(TestCase):
    """Tests for login, signup, and logout flows."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123!"
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_signup_page_loads(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_login_success_redirects(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "testpass123!"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_login_failure_stays_on_page(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)

    def test_signup_creates_user(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "password1": "Str0ngP@ss!",
                "password2": "Str0ngP@ss!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_home_requires_login(self):
        """Unauthenticated users should be redirected to login."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("next", response.url)

    def test_home_accessible_when_logged_in(self):
        self.client.login(username="testuser", password="testpass123!")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_logout_redirects_to_login(self):
        self.client.login(username="testuser", password="testpass123!")
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))


# ─── Integration Tests: Calculator Views ─────────────────────────────────────


class CalculatorViewTest(TestCase):
    """Tests for the calculator POST actions."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="calcuser", password="testpass123!"
        )
        self.client.login(username="calcuser", password="testpass123!")

    def test_addition(self):
        response = self.client.post(
            reverse("home"),
            {"num1": "5", "num2": "3", "action": "addition"},
        )
        self.assertContains(response, "8")

    def test_subtraction(self):
        response = self.client.post(
            reverse("home"),
            {"num1": "10", "num2": "4", "action": "subtraction"},
        )
        self.assertContains(response, "6")

    def test_multiplication(self):
        response = self.client.post(
            reverse("home"),
            {"num1": "3", "num2": "7", "action": "multiplication"},
        )
        self.assertContains(response, "21")

    def test_division(self):
        response = self.client.post(
            reverse("home"),
            {"num1": "10", "num2": "2", "action": "division"},
        )
        self.assertContains(response, "5")

    def test_division_by_zero_shows_error(self):
        response = self.client.post(
            reverse("home"),
            {"num1": "5", "num2": "0", "action": "division"},
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_input(self):
        response = self.client.post(
            reverse("home"),
            {"num1": "abc", "num2": "3", "action": "addition"},
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_operation(self):
        response = self.client.post(
            reverse("home"),
            {"num1": "1", "num2": "2", "action": "modulus"},
        )
        self.assertEqual(response.status_code, 200)


# ─── Integration Tests: Calculation History ──────────────────────────────────


class CalculationHistoryTest(TestCase):
    """Tests for the CalculationHistory model and persistence."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="historyuser", password="testpass123!"
        )
        self.client.login(username="historyuser", password="testpass123!")

    def test_calculation_saved_to_history(self):
        self.client.post(
            reverse("home"),
            {"num1": "10", "num2": "2", "action": "multiplication"},
        )
        self.assertEqual(CalculationHistory.objects.count(), 1)
        calc = CalculationHistory.objects.first()
        self.assertEqual(calc.result, 20.0)
        self.assertEqual(calc.user, self.user)
        self.assertEqual(calc.operation, "multiplication")

    def test_history_displayed_on_page(self):
        CalculationHistory.objects.create(
            user=self.user, num1=5, num2=3, operation="addition", result=8,
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "8")

    def test_division_by_zero_not_saved(self):
        self.client.post(
            reverse("home"),
            {"num1": "5", "num2": "0", "action": "division"},
        )
        self.assertEqual(CalculationHistory.objects.count(), 0)

    def test_history_belongs_to_user(self):
        """Each user should only see their own history."""
        other_user = User.objects.create_user(
            username="otheruser", password="testpass123!"
        )
        CalculationHistory.objects.create(
            user=other_user, num1=1, num2=1, operation="addition", result=2,
        )
        response = self.client.get(reverse("home"))
        # The other user's calculation should not appear
        history = response.context["history"]
        self.assertEqual(len(history), 0)

    def test_model_str(self):
        calc = CalculationHistory.objects.create(
            user=self.user, num1=5.5, num2=3.5, operation="addition", result=9.0,
        )
        self.assertIn("addition", str(calc))
