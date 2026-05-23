"""
Arithmetic operations module.

Provides pure functions for calculator operations with proper error handling
and structured logging.
"""
import logging

logger = logging.getLogger(__name__)


class DivisionByZeroError(Exception):
    """Raised when division by zero is attempted."""
    pass


def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    logger.debug("Adding %s + %s", a, b)
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of two numbers."""
    logger.debug("Subtracting %s - %s", a, b)
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of two numbers."""
    logger.debug("Multiplying %s * %s", a, b)
    return a * b


def divide(a: float, b: float) -> float:
    """Return the quotient of two numbers.

    Raises:
        DivisionByZeroError: If b is zero.
    """
    if b == 0:
        logger.warning("Division by zero attempted: %s / %s", a, b)
        raise DivisionByZeroError("Cannot divide by zero")
    logger.debug("Dividing %s / %s", a, b)
    return a / b
