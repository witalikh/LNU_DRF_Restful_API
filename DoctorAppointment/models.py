from django.db import models


class ModelConsts:

    AVAILABLE_REQUESTS = 3
    NAME_WORDS_COUNT = (2, 10)
    INVALID_NAME = (f"Only letters or hyphens, "
                    f"from {NAME_WORDS_COUNT[0]} "
                    f"to {NAME_WORDS_COUNT[1]} words")


class DoctorAppointment(models.Model):
    """
    Django model for Doctor Arrangement
    """

    user_id = models.IntegerField(verbose_name="user's id")
    item_id = models.AutoField(auto_created=True,
                               primary_key=True,
                               verbose_name="number of appointment")

    doctor_fullname = models.CharField(verbose_name='doctor', max_length=256)

    start_datetime = models.DateTimeField(verbose_name="doctor meeting start date and time")
    end_datetime = models.DateTimeField(verbose_name='doctor meeting end date and time')
