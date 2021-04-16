from django.db import models
from django_countries.fields import CountryField
from core import models as core_models


# Create your models here.


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True  # 데이터베이스에서 참조하지 않는 것. admin 패널에서 확인하는 것과는 다른 문제.


class RoomType(AbstractItem):

    """ RoomType Object Definition """

    class Meta:
        verbose_name = "Room Type"
        # ordering = ["created"]
        # AbstractItem 의 create (core 의 TimeStampedModel) 시간 순서대로 정렬.


class Amenity(AbstractItem):

    """ AmenityType Object Definition """

    class Meta:
        verbose_name_plural = "Amenities"
        # admin 패널에서 자동으로 Amenitys 로 표기되는 걸 커스텀 하기.


class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """ HouseRule Model Definition """

    class Meta:
        verbose_name_plural = "House Rule"


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField()
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)
    # "Room" 처리한 이유는 Room 클래스가 아래에 있기 떄문에 Photo 를 아래로 옮기거나 string 처리해서 읽을 수 있음. 장고의 기능.

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    # foreignKey 는 many to one 구조. 방은 host 를 한 명 밖에 가질 수 없지만 host 는 여러 room 을 가질 수 있음.
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    # many to many 구조를 사용해야할 때는 ManyToMajyField 를 사용한다.
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name
