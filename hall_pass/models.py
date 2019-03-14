from datetime import datetime
import jsonschema

from django.contrib.postgres.fields import JSONField
from django.db import models

##### generic models #####

DATE_FORMAT = "%d %B %Y"
DATETIME_FORMAT = "%d %B %Y %I:%M%p"

SCHEDULE_SCHEMA = {
    "description": "A representation of a course's precise meeting times",
    "type": "array",
    "uniqueItems": True,
    "items": { "$ref": "#/definitions/period" },
    "definitions": {
        "period" : {
            "type": "object",
            "required": [ "start_time", "end_time" ],
            "properties": {
                "start_time": { "type": "string", "format": "date-time" },
                "end_time": { "type": "string", "format": "date-time" }
            }
        }
    }
}


def schedule_validator(value):
    """Validate a Schedule.meetings JSON field.

    `Schedule.meetings` are implemented as an array of dictionaries, where each element corresponds
    to a date and time at which a `Course` will meet (a "period"). They must be valid JSON (see
    `SCHEDULE_SCHEMA`). Each period must include a `start_time` and an `end_time` field,  which
    must be valid serializations of `datetime` objects. Each `start_time` must come before its
    corresponding `end_time`, and no two periods ma overlap. The list need not be sorted, but it
    will be sorted upon saving.

    """
    def check_single_item(item):
        """Ensure the period start time is before the end time."""
        assert (
            datetime.strptime(item["start_time"], DATETIME_FORMAT)
            <
            datetime.strptime(item["end_time"], DATETIME_FORMAT)
        ), "Invalid schedule item {}: Period start times must precede end times.".format(
            item
        )

    def check_adjacent_items(prev, cur):
        """Ensure two periods do not overlap; prev.start_time must precede cur.start_time."""
        assert (
            datetime.strptime(prev["end_time"], DATETIME_FORMAT)
            <
            datetime.strptime(cur["start_time"], DATETIME_FORMAT)
        ), "Invalid schedule combination {} {}: New period starts before old ends.".format(
            prev, cur
        )

    # Assert that the value is of the valid JSON schema
    jsonschema.validate(instance=value, schema=SCHEDULE_SCHEMA)

    # Sort the array
    # NOTE: sorting here is sort of wasteful because we will have to sort again before saving;
    #       however, this is more efficient than comparing every combination of periods, which would
    #       take O(n!).
    sorted_value = sorted(value, key=lambda x:x["start_time"])

    # Assert that the periods are valid and do not overlap
    check_single_item(sorted_value[0])
    for i in range(1, len(sorted_value)):
        check_single_item(sorted_value[i])
        check_adjacent_items(sorted_value[i-1], sorted_value[i])


class Schedule(models.Model):
    """Database representation of the dates and times at which a `Course` meets."""
    name = models.CharField(max_length=50)
    meetings = JSONField(
        "Meeting Times",
        validators=[schedule_validator],
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Override the save() method to sort() self.meetings by "start_time"."""
        self.meetings = sorted(self.meetings, key=lambda x:x["start_time"])
        super().save(*args, **kwargs)


class Teacher(models.Model):
    """Database representation of a teacher at the school."""
    teacher_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Student(models.Model):
    """Database representation of a student at the school."""
    student_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    current_absence = models.ForeignKey(
        'Absence',
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        related_name='+'
    )
    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Course(models.Model):
    """Database representation of a course offered at the school."""
    course_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    def __str__(self):
        return "{}: {} {}".format(self.teacher, self.name, self.schedule)


class Absence(models.Model):
    """Database representation of a student's absence from a course."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    time_out = models.DateTimeField('time out')
    time_in = models.DateTimeField(
        'time in',
        default=None,
        blank=True,
        null=True
    )
    # NOTE: reason should have choices. Perhaps easier to implement in HTML forms, though,
    #       in case they change down the road or "other" is desired.
    reason = models.CharField(max_length=200)
    def __str__(self):
        return "{} checkout at {}".format(self.student, self.time_out)

##### Timberlane-specific models #####

class TimberlaneDaysOff(models.Model):
    """Database representation of special days off from school during a `Semester`."""
    name = models.CharField(max_length=50)
    start_date = models.DateField('start date')
    end_date = models.DateField('end date')
    def __str__(self):
        return "{}: {}".format(
            self.name, self.start_date.strftime(DATE_FORMAT)
        ) if self.start_date == self.end_date else "{}: {}-{}".format(
            self.name, self.start_date.strftime(DATE_FORMAT), self.end_date.strftime(DATE_FORMAT)
        )

class TimberlaneSemester(models.Model):
    """Database representation of a semester at the Timberlane school."""

    YEAR_CHOICES = (
        ('2019', '2019'),
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
    )

    SEASON_CHOICES = (
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
    )

    year=models.CharField(max_length=4, choices=YEAR_CHOICES)
    season=models.CharField(max_length=6, choices=SEASON_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    days_off = models.ManyToManyField(
        TimberlaneDaysOff,
        default=list,
        blank=True,
    )

    def __str__(self):
        return "{} {}".format(self.season, self.year)

class TimberlaneSchedule(models.Model):
    """Database representation of a `Course` `Schedule` specific to the Timberlane school.

    This class provides a layer of abstraction around creating `Schedule` objects for the Timberlane
    school, so that users need not enter each individual day on which a `Course` will meet to build
    the schedule. Instead, only the block, period, and semester are needed, and a one-to-one
    `Schedule` object will automatically be generated based on Timberlane's scheduling rules.

    """
    BLOCK_CHOICES = (
        ('A Block', 'A Block'),
        ('B Block', 'B Block'),
    )
    PERIOD_CHOICES = (
        ('1st Period', '1st Period'),
        ('2nd Period', '2nd Period'),
        ('3rd Period', '3rd Period'),
        ('4th Period', '4th Period'),
        ('5th Period', '5th Period'),
    )

    block=models.CharField(max_length=10, choices=BLOCK_CHOICES)
    period=models.CharField(max_length=20, choices=PERIOD_CHOICES)
    semester=models.ForeignKey(
        TimberlaneSemester,
        on_delete=models.CASCADE
    )
    schedule=models.OneToOneField(
        Schedule,
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def get_schedule_meeting_times(self):
        # TODO: implement logic of how to get meeting times for Timberlane based on self.block,
        #       self.period, and self.semester
        return [
            {
                "start_time": "12 March 2019 9:00AM",
                "end_time": "12 March 2019 10:00AM"
            },
            {
                "start_time": "14 March 2019 9:00AM",
                "end_time": "14 March 2019 10:00AM"
            },
        ]

    def save(self, *args, **kwargs):
        """Override the `save()` method to build the exact meeting times of this course.

        The meeting times must be passed to the corresponding `Schedule` in the form of an array of
        stringified `datetime` objects. Once this is created, the one-to-one-mapped `Schedule`
        object is created and both are saved.

        """
        schedule = Schedule(
            name=str(self),
            meetings=self.get_schedule_meeting_times()
        )
        schedule.save()
        self.schedule = schedule
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} {} {}".format(self.block, self.period, self.semester)
