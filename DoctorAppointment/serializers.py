from rest_framework import serializers

from algorithms.validators import ValidateName
from .models import DoctorAppointment, ModelConsts


class DoctorAppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorAppointment
        fields = "__all__"
        read_only_fields = ["user_id", "item_id"]

        extra_kwargs = {
            "doctor_fullname": {
                "validators": [
                    ValidateName(*ModelConsts.NAME_WORDS_COUNT,
                                 ModelConsts.INVALID_NAME),
                ]
            }
        }

    def validate(self, data):
        """
        Main validation function, validates entries while serialization
        """

        # get user_id directly from request
        request = self.context.get("request")
        user = getattr(request, "user", None)

        # prepare fields for check-up
        user_id = user.pk
        start_datetime = data["start_datetime"]
        end_datetime = data["end_datetime"]

        # get all records with the same user_id
        obj_data = DoctorAppointment.objects.filter(user_id__exact=user_id)

        # data for validation
        # count records (for bounding the count of meetings per user)
        existing_records = obj_data.count()

        # find arrangements overlap
        overlapping_start = obj_data.filter(start_datetime__gte=start_datetime,
                                            start_datetime__lte=end_datetime).exists()

        overlapping_end = obj_data.filter(end_datetime__gte=start_datetime,
                                          end_datetime__lte=end_datetime).exists()

        enveloping = obj_data.filter(start_datetime__lte=start_datetime,
                                     end_datetime__gte=end_datetime).exists()

        # validation
        conditions = [
            existing_records < ModelConsts.AVAILABLE_REQUESTS,
            start_datetime < end_datetime,
            not overlapping_start,
            not overlapping_end,
            not enveloping,
        ]

        # prepared messages for errors
        errors = [
            ("__all__", "The number of doctor arrangements is out of available"),
            ("start_datetime", "Start datetime cannot be after end datetime"),
            ("start_datetime", "Datetime range of meeting cannot start during another one"),
            ("end_datetime", "Datetime range of meeting cannot end during another one"),
            ("end_datetime", "Current datetime range envelops another"),
        ]

        # rise errors or return validated
        dict_of_errors = {}
        for index, (condition, msg) in enumerate(zip(conditions, errors)):
            if not condition:
                dict_of_errors[msg[0]] = msg[1]

        if len(dict_of_errors) != 0:
            raise serializers.ValidationError(dict_of_errors)

        return data
