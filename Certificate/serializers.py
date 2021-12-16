from rest_framework import serializers
from datetime import date, timedelta

from .models import Certificate, ModelConsts
from algorithms.validators import ValidateName, ValidatePattern


class SerializerConsts:
    FORMAT_ERRORS = {
        "username": f"Only letters or hyphens, "
                    f"from {ModelConsts.NAME_WORDS_COUNT[0]} "
                    f"to {ModelConsts.NAME_WORDS_COUNT[1]} words",

        "international_passport": "Mismatch between pattern XXYYYYYY "
                                  "where X-letters, Y-digits",
    }

    EXTRA_VALIDATORS = {
        "username": [
            ValidateName(*ModelConsts.NAME_WORDS_COUNT, FORMAT_ERRORS["username"]),
        ],
        "international_passport": [
            ValidatePattern(ModelConsts.INTERNATIONAL_PASSPORT_PATTERN,
                            FORMAT_ERRORS["international_passport"]),
        ],

    }


class CertificateSerializer(serializers.ModelSerializer):
    """
    Serializer of Certificate model
    """
    class Meta:

        model = Certificate
        fields = "__all__"
        read_only = ("id", )

        extra_kwargs = {
            "username": {
                "validators": SerializerConsts.EXTRA_VALIDATORS["username"],
            },

            "international_passport": {
                "validators": SerializerConsts.EXTRA_VALIDATORS["international_passport"]
            },
        }

    def validate(self, data):
        """
        Main validation function, validates entries while serialization
        """

        def subtract_years(date_: date, years):
            try:
                return date_.replace(year=date_.year-years)

            # leap year cases
            except ValueError:
                return date_.replace(year=date_.year - years, day=date_.day-1)

        # conditions prerequisites
        today_date = date.today()

        # passport bounds
        oldest = subtract_years(today_date, ModelConsts.OLDEST_PASSPORT)
        newest = subtract_years(today_date, ModelConsts.NEWEST_PASSPORT)

        # start date bounds
        min_vaccination = subtract_years(data["date_of_birth"], -ModelConsts.MIN_VACCINATION_AGE)
        max_delay = today_date + timedelta(days=ModelConsts.MAX_CERT_DELAY)

        # conditions for passing the validation
        conditions = [

            oldest < data["date_of_birth"] <= newest,
            min_vaccination <= data["start_date"],
            data["start_date"] <= max_delay,
            data["start_date"] < data["end_date"]
        ]

        # statements when conditions violated
        errors = [
            ("date_of_birth", f"invalid date of birth, not between "
                              f"{ModelConsts.OLDEST_PASSPORT} and "
                              f"{ModelConsts.NEWEST_PASSPORT} years"),

            ("start_date", f"start_date is too early, "
                           f"under {ModelConsts.MIN_VACCINATION_AGE} years old"),

            ("start_date", f"start_date is too late, "
                           f"after {ModelConsts.MAX_CERT_DELAY} days"),

            ("end_date", "end_date is too early, before start date")
        ]

        # collect errors in one dict
        dict_of_errors = {}
        for index, condition in enumerate(conditions):
            if not condition:
                dict_of_errors[errors[index][0]] = errors[index][1]

        # raise all errors in one pull
        if len(dict_of_errors) != 0:
            raise serializers.ValidationError(dict_of_errors)

        return data
