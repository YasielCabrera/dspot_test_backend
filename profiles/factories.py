import factory
from factory import fuzzy  # noqa
from faker import Faker
from random import randint
from .models import Profile, Photo, Status

fake = Faker()


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo

    image = factory.django.ImageField(
        color=factory.fuzzy.FuzzyChoice(
            ['blue', 'yellow', 'green', 'orange', 'red', 'indigo'])
    )
    profile = factory.SubFactory('profiles.factories.SimpleProfileFactory')


class StatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status

    text = factory.Faker('catch_phrase')
    profile = factory.SubFactory('profiles.factories.SimpleProfileFactory')


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    img = factory.django.ImageField(
        color=factory.fuzzy.FuzzyChoice(
            ['blue', 'yellow', 'green', 'orange', 'red', 'indigo'])
    )
    phone = factory.Faker('phone_number')
    address_1 = factory.Faker('address')
    city = factory.Faker('city')
    state = factory.Faker('city_suffix')
    zipcode = factory.Faker('zipcode')
    bio = factory.Faker('text')
    temper = factory.Faker('catch_phrase')
    available = factory.Faker('boolean')

    @factory.post_generation
    def friends(self, create, extracted):
        if not create or not extracted:
            return

        self.friends.add(*extracted)


class FullProfileFactory(ProfileFactory):
    @factory.post_generation
    def friends(self, create, extracted):
        if create and extracted:
            self.friends.add(*extracted)
            return

        if create:
            profiles = list(Profile.objects.exclude(pk=self.pk))
            if len(profiles) > 0:
                friends = []
                count = randint(1, len(profiles))
                while count > 0:
                    index = randint(0, len(profiles) - 1)
                    friends.append(profiles.pop(index))
                    count -= 1
                self.friends.add(*friends)

    @factory.post_generation
    def photos(self, create, extracted):
        if create and extracted:
            self.photos.add(*extracted)
            return

        if create:
            photos = []
            for _ in range(randint(1, 10)):
                photos.append(PhotoFactory(profile=self))
            self.photos.add(*photos)

    @factory.post_generation
    def statuses(self, create, extracted):
        if create and extracted:
            self.statuses.add(*extracted)
            return

        if create:
            statuses = []
            for _ in range(randint(1, 10)):
                statuses.append(StatusFactory(profile=self))
            self.statuses.add(*statuses)
