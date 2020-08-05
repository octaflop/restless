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

    @classmethod
    def generate_campground(cls, num_campsites=10, num_campers=4, hosts=None):
        hosts = hosts or [CampHostFactory.create() for _ in range(5)]

        campground = cls.create()
        for host in hosts:
            host.campgrounds.add(campground)
        for num in range(num_campsites):
            campsite = CampsiteFactory.create(campground=campground)
            for ncamper in range(num_campers):
                camper = CamperFactory.create(campsite=campsite)
        return campground


class CampsiteFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('street_name')
    location = factory.Faker('street_name')

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
