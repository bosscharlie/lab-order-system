from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserInfo(AbstractUser):
    tel = models.CharField(max_length=32, verbose_name="联系电话")


class Room(models.Model):
    caption = models.CharField(max_length=32, verbose_name="会议室名称")
    capacity = models.IntegerField(verbose_name="可容纳人数")

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = "会议室信息"
        verbose_name_plural = verbose_name


class Book(models.Model):
    """预定信息"""
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    time_choice = (
        (1, "8:00~9:00"),
        (2, "9:00~10:00"),
        (3, "10:00~11:00"),
        (4, "11:00~12:00"),
        (5, "12:00~13:00"),
        (6, "13:00~14:00"),
        (7, "14:00~15:00"),
        (8, "15:00~16:00"),
        (9, "16:00~17:00"),
        (10, "17:00~18:00"),
    )

    time_id = models.IntegerField(choices=time_choice)

    def __str__(self):
        return str(self.user) + "预定了" + str(self.room)

    class Meta:
        verbose_name = "预定信息"
        verbose_name_plural = verbose_name
        unique_together = (
            ("room", "date", "time_id"),
        )
