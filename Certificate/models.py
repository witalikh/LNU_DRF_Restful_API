from django.db import models


class ModelConsts:
    """
    Class for important model constants, for code flexibility
    """

    NAME_WORDS_COUNT = (2, 10)

    INTERNATIONAL_PASSPORT_PATTERN = "[a-zA-z]{2}[0-9]{6}"

    # requirement for choices field
    AVAILABLE_VACCINES = [
        "Pfizer",
        "Moderna",
        "AstraZeneca",
        "CoronaVac",
        "CoviShield",
        "Jannsen",
    ]

    AVAILABLE_VACCINES_CHOICES = [(vaccine, vaccine) for vaccine in AVAILABLE_VACCINES]

    OLDEST_PASSPORT = 125
    NEWEST_PASSPORT = 14

    MIN_VACCINATION_AGE = 14
    MAX_CERT_DELAY = 14


class Certificate(models.Model):
    """
    Django model for Covid Certificate
    """

    username = models.CharField(max_length=256)
    international_passport = models.CharField(max_length=8)
    date_of_birth = models.DateField()

    start_date = models.DateField()
    end_date = models.DateField()

    vaccine = models.CharField(max_length=64,
                               choices=ModelConsts.AVAILABLE_VACCINES_CHOICES)
