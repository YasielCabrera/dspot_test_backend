from rest_framework import serializers

from profiles.models import Profile, Photo, Status


class ProfileSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    statuses = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'img', 'first_name', 'last_name', 'phone', 'address_1',
                  'city', 'state', 'zipcode', 'bio', 'temper', 'available', 'photos', 'statuses']
        depth = 1

    def get_photos(self, obj) -> list[str]:
        request = self.context.get('request')
        print('>>>>', dir(self))
        return map(
            lambda photo: request.build_absolute_uri(photo.image.url),
            Photo.objects.filter(profile=obj)
        )

    def get_statuses(self, obj) -> list[str]:
        return map(
            lambda status: status.text,
            Status.objects.filter(profile=obj)
        )
