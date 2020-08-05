from django import test

from restless.campgrounds.tests.factories import CampHostFactory, CampgroundFactory, CampsiteFactory, CamperFactory


# example for now, as I'm running into testing issues :/
class ModelTestCase(test.TestCase):
    def test_relationships(self):
        campground = CampgroundFactory.create()
        campsite_1 = CampsiteFactory.create(campground=campground)
        campsite_2 = CampsiteFactory.create(campground=campground)
        campsite_3 = CampsiteFactory.create(campground=campground)
        camp_host = CampHostFactory.create(campgrounds=[campground])
        camper_1 = CamperFactory.create(campsite=campsite_1)
        camper_2 = CamperFactory.create(campsite=campsite_1)
        camper_3 = CamperFactory.create(campsite=campsite_2)
        camper_4 = CamperFactory.create(campsite=campsite_2)
        camper_5 = CamperFactory.create(campsite=campsite_3)

        assert campsite_1.campers.count() > 1
        assert camper_1 in campsite_1.campers.all()
        assert camper_2 in campsite_1.campers.all()
        assert camper_3 in campsite_2.campers.all()
        assert camper_4 in campsite_2.campers.all()
        assert camper_5 in campsite_3.campers.all()
        assert camp_host in campsite_1.hosts
