from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserInfo(AbstractUser):
    # coursename=models.CharField(max_length=32,verbose_name="课程名称")
    # printel=models.CharField(max_length=32,verbose_name="负责人及联系电话")
    # bookertel=models.CharField(max_length=32,verbose_name="预约人及电话")
    # adminer=models.CharField(max_length=32,verbose_name="实验室审批人")
    # tel = models.CharField(max_length=32, verbose_name="联系电话")
    pass


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
        (1, "8:00~9:35"),
        (2, "9:50~12:05"),
        (3, "12:05~13:30"),
        (4, "13:30~15:05"),
        (5, "15:20~17:55"),
        (6, "18:00~19:20"),
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
