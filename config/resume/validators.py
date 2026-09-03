from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r"^09\d{9}$",
    message="Phone number must start with 09 and have 11 digits."
)