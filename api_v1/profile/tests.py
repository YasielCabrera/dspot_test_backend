from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from parameterized import parameterized

from profiles.factories import ProfileFactory


class ProfileTests(APITestCase):
    profile_list_url = reverse('profile-list')

    def test_get_all_profiles_empty(self):
        response_empty = self.client.get(self.profile_list_url, format='json')
        self.assertEqual(response_empty.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_empty.data), 0)

    def test_get_all_profiles(self):
        profile = ProfileFactory()
        response = self.client.get(self.profile_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], profile.first_name)

    def test_profile_detail_404(self):
        profile_detail_url = reverse('profile-detail', args=[1])
        response = self.client.get(profile_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_profile_detail(self):
        profile = ProfileFactory()
        profile_detail_url = reverse('profile-detail', args=[profile.pk])
        response = self.client.get(profile_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FriendTests(APITestCase):

    def test_get_friends_of_profile_404(self):
        friend_detail_url = reverse('friend-detail', args=[1])
        response = self.client.get(friend_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_friends_of_profile_empty(self):
        friend_detail_url = reverse('friend-detail', args=[1])
        response = self.client.get(friend_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_friends_of_profile(self):
        a = ProfileFactory()
        b = ProfileFactory(friends=(a, ))
        friend_detail_url = reverse('friend-detail', args=[b.pk])
        response = self.client.get(friend_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @parameterized.expand([
        ([(1, 2), (1, 3), (3, 5), (2, 4), (5, 4)], 1, 8, []),
        ([(1, 2), (1, 3), (3, 5), (2, 4), (5, 4)], 1, 4, [2]),
        ([(1, 2), (1, 3), (3, 5), (2, 4), (5, 4)], 4, 1, [2]),
        ([(1, 2), (1, 3), (3, 5), (2, 4), (5, 4)], 1, 2, []),
        ([(1, 2), (1, 3), (3, 5), (2, 4), (5, 4), (4, 6)], 1, 6, [2, 4]),
    ])
    def test_shorter_connection(self, graph, from_id, to_id, expected):
        users = {}
        def key(x): return f'user{x}'
        for a, b in graph:
            u_a = users[key(a)] if key(a) in users else ProfileFactory(
                first_name=key(a))
            users[key(a)] = u_a
            u_b = users[key(b)] if key(b) in users else ProfileFactory(
                first_name=key(b))
            users[key(b)] = u_b
            u_a.friends.add(u_b)

        url = reverse('friend-shorter-connection', args=[
            users[key(from_id)].pk if key(from_id) in users else from_id,
            users[key(to_id)].pk if key(to_id) in users else to_id
        ])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # DB ids could not match with the provided ids
        normalized_expected = []
        for i in expected:
            normalized_expected.append(
                i if key(i) not in users else users[key(i)].pk)

        self.assertEqual(response.data, normalized_expected)
