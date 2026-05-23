from django.db import models
from django.contrib.auth.models import User


class CalculationHistory(models.Model):
    """Stores each calculation performed by a user."""

    OPERATION_CHOICES = [
        ("addition", "Addition"),
        ("subtraction", "Subtraction"),
        ("multiplication", "Multiplication"),
        ("division", "Division"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="calculations"
    )
    num1 = models.FloatField()
    num2 = models.FloatField()
    operation = models.CharField(max_length=20, choices=OPERATION_CHOICES)
    result = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Calculation histories"

    def __str__(self):
        return f"{self.num1} {self.operation} {self.num2} = {self.result}"
