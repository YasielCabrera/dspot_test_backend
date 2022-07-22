from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from dijkstar import Graph, find_path, NoPathError


class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='profiles/')
    # phone number following (E.164 standard, https://en.wikipedia.org/wiki/E.164)
    phone = PhoneNumberField()
    address_1 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    bio = models.TextField()
    temper = models.CharField(max_length=255)
    available = models.BooleanField(default=False)

    friends = models.ManyToManyField('self', blank=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    @staticmethod
    def shorter_connection(from_id, to_id):
        profiles = Profile.objects.all()
        graph = Graph()
        for profile in profiles:
            for friend in profile.friends.all():
                graph.add_edge(profile.pk, friend.pk, 1)
        
        nodes = []
        try:
            path_info = find_path(graph, from_id, to_id)
            nodes = path_info[0]
            if len(nodes) >= 2:
                nodes.remove(from_id)
                nodes.remove(to_id)
        except NoPathError:
            return []
        return nodes


class Photo(models.Model):
    image = models.ImageField(upload_to='photos')
    profile = models.ForeignKey(
        Profile, related_name='photos', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.image)


class Status(models.Model):
    text = models.CharField(max_length=255)
    profile = models.ForeignKey(
        Profile, related_name='statuses', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.text
