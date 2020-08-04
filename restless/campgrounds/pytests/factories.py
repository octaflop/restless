import factory


class CampHostFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'campgrounds.CampHost'
        django_get_or_create = ('name',)


class CampgroundFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'campgrounds.Campground'
        django_get_or_create = ('name',)


class CampsiteFactory(factory.django.DjangoModelFactory):
    campground = factory.SubFactory(CampgroundFactory)

    class Meta:
        model = 'campgrounds.Campsite'
        django_get_or_create = ('name',)

class CamperFactory(factory.django.DjangoModelFactory):
    campsite = factory.SubFactory(CampsiteFactory)

    class Meta:
        model = 'campgrounds.Camper'
        django_get_or_create = ('name',)
