from django.db import models


class NameMixin(models.Model):
    """Because I don't want to write the same thing over and over"""
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__repr__} {self.name}"


class CampHost(NameMixin):
    """Admins of camp campgrounds"""
    campgrounds = models.ManyToManyField('campgrounds.Campground')


class Camper(NameMixin):
    """Someone staying at a campsite"""
    campsite = models.ForeignKey('campgrounds.Campsite', on_delete=models.CASCADE,
                                 related_name='campers')

    def __str__(self):
        ret = super(Camper).__str__()
        return f"{ret} staying at {self.campsite.name}"


class Campsite(NameMixin):
    """A reservable / occupy-able location on a camp ground"""
    tent_only = models.BooleanField(default=True)
    location = models.CharField(max_length=255)
    campground = models.ForeignKey('campgrounds.Campground', on_delete=models.CASCADE,
                                   related_name='campsites')

    def __str__(self):
        ret = super(Camper).__str__()
        return f"{ret} a campsite at {self.campground.name}"

    @property
    def hosts(self):
        return self.campground.camphost_set.all()


class Campground(NameMixin):
    """A set of campsites in a location"""
    established = models.DateTimeField(auto_now=True)

    def __str__(self):
        ret = super(Campground).__str__()
        fmt = r"%Y-%m-%d %H:%M"
        return f"{ret} established {self.established.strftime(fmt)}"
