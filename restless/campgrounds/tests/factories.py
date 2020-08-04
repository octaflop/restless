import factory

from restless.campgrounds.models import CampHost, Campground, Camper, Campsite


class CampHostFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('first_name')

    class Meta:
        model = CampHost
        django_get_or_create = ('name',)

    @factory.post_generation
    def groups(self, create, campgrounds, **kwargs):
        if not create:
            return

        if campgrounds:
            for campground in campgrounds:
                self.campgrounds.add(campground)


class CampgroundFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('street_name')

    class Meta:
        model = Campground
        django_get_or_create = ('name',)


class CampsiteFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('street_name')
    campground = factory.SubFactory(CampgroundFactory)

    class Meta:
        model = Campsite
        django_get_or_create = ('name',)

class CamperFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    campsite = factory.SubFactory(CampsiteFactory)

    class Meta:
        model = Camper
        django_get_or_create = ('name',)
