import os
import pickle
import requests
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class YouTube:
    def __init__(self):
        self.headers = None
        self.refresh_token = None
        self.credentials = None
        self.url = 'https://youtube.googleapis.com/youtube/v3/'

    def authenticate(self):
        """
        This method stores the user's first login credentials for future use.
        If there are no valid credentials, a Google login pop-up will appear
        and ask the user to allow the app to make changes to your account.
        """

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)

        # If there are no valid credentials available, then either refresh the token or log in.
        if not self.credentials or not self.credentials.valid:

            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secrets.json',
                    scopes=[
                        'https://www.googleapis.com/auth/youtube'
                    ]
                )

                flow.run_local_server(port=8080, prompt='consent',
                                      authorization_prompt_message='')
                self.credentials = flow.credentials

                # Save the credentials for the next run
                with open('token.pickle', 'wb') as f:
                    pickle.dump(self.credentials, f)

        self.refresh_token = build('youtube', 'v3', credentials=self.credentials)
        self.headers = {'Authorization': f'Bearer {self.credentials.token}'}

    @staticmethod
    def request_status(request):
        if request.status_code // 10 < 30:
            print('Request successful!')
        else:
            print('Request not successful.')
            print(request.text)

    def _build_resource(self, api):
        return f'{self.url}{api}'

    def my_playlists(self):
        """Lists all the playlists of your YouTube channel in JSON format"""

        params = dict(
            part='snippet,contentDetails',
            mine=True,
        )

        response = requests.get(
            url=self._build_resource('playlists'),
            params=params,
            headers=self.headers
        )

        results = []

        try:

            for playlist in response.json()['items']:
                results.append(playlist['id'])

            # Get next page token
            next_page_token = response.json()['nextPageToken']

            # Loop through the pages of the response
            while next_page_token:

                params = dict(
                    part='snippet,contentDetails',
                    mine=True,
                    pageToken=next_page_token
                )
                response = requests.get(
                    url=self._build_resource('playlists'),
                    params=params,
                    headers=self.headers
                )

                # Update the response and the next page token
                data = response.json()
                next_page_token = data['nextPageToken']

                # Append the video id's from the current page
                for playlist in response.json()['items']:
                    results.append(playlist['id'])

        except KeyError:

            # If there are no next pages we need to check if this is not the first page before we append anything
            for playlist in response.json()['items']:
                results.append(playlist['id'])

        self.request_status(response)
        return results

    def create_playlist(self, title, description=None):
        """Creates a new playlist on your YouTube channel"""
        params = dict(
            part='snippet,status'
        )

        payload = dict(
            snippet=dict(
                title=title,
                description=description
            ),
            status=dict(
                privacyStatus='public'
            ),
        )

        response = requests.post(
            url=self._build_resource('playlists'),
            params=params,
            json=payload,
            headers=self.headers,
        )

        self.request_status(response)
        return response.json()['id']

    def edit_playlist_details(
            self, playlist_id,
            new_title='Sample edit',
            new_description='Sample description',
            privacy_status='public'
    ):
        """Edit one of your account's playlists' details"""

        params = dict(
            part='id,snippet,status',
        )

        payload = dict(
            id=playlist_id,
            snippet=dict(
                title=new_title,
                description=new_description
            ),
            status=dict(
                privacyStatus=privacy_status
            ),
        )

        response = requests.put(
            url=self._build_resource('playlists'),
            params=params,
            json=payload,
            headers=self.headers,
        )

        self.request_status(response)
        return response.json()

    def retrieve_playlist_details(self, playlist_id):
        """Retrieves the details about a playlist from your channel"""

        params = dict(
            part='snippet',
            id=playlist_id
        )

        response = requests.get(
            url=self._build_resource('playlists'),
            params=params,
            headers=self.headers
        )

        self.request_status(response)
        return response.json()

    def add_video_to_playlist(self, playlist_id, video_id):
        """Adds a video to a specified playlist on your channel"""

        params = dict(
            part='snippet'
        )

        payload = dict(
            snippet=dict(
                playlistId=playlist_id,
                resourceId=dict(
                    kind='youtube#video',
                    videoId=video_id
                )
            )
        )

        response = requests.post(
            url=self._build_resource('playlistItems'),
            params=params,
            json=payload,
            headers=self.headers,
        )

        self.request_status(response)
        return response.json()

    def remove_video_from_playlist(self, video_id):
        """Removes a video from your channel based on its ID"""

        params = dict(
            part='id'
        )

        payload = dict(
            id=video_id
        )

        response = requests.delete(
            url=self._build_resource('playlistItems'),
            params=params,
            json=payload,
            headers=self.headers
        )

        self.request_status(response)
        return response.json()

    def delete_playlist(self, playlist_id):
        """Deletes a playlist from your account"""

        params = dict(
            part='id'
        )

        payload = dict(
            id=playlist_id
        )

        response = requests.delete(
            url=self._build_resource('playlists'),
            params=params,
            json=payload,
            headers=self.headers
        )

        self.request_status(response)
        return response.json()

    def retrieve_videos_from_playlist(self, playlist_id):
        """Retrieves all the songs from your playlist"""

        songs_data = []

        params = dict(
            part='snippet,contentDetails',
            playlistId=playlist_id
        )

        response = requests.get(
            url=self._build_resource('playlistItems'),
            params=params,
            headers=self.headers,
        )

        # Append every video id of the playlist page to songs_data.
        try:

            for song in response.json()['items']:
                songs_data.append(song['snippet']['resourceId']['videoId'])

            # Get next page token
            next_page_token = response.json()['nextPageToken']

            # Loop through the pages of the response
            while next_page_token:

                params = dict(
                    part='snippet',
                    playlistId=playlist_id,
                    pageToken=next_page_token
                )
                response = requests.get(
                    url=self._build_resource('playlistItems'),
                    params=params,
                    headers=self.headers,
                )

                # Update the response and the next page token
                data = response.json()
                next_page_token = data['nextPageToken']

                # Append the video id's from the current page
                for song in response.json()['items']:
                    songs_data.append(song['snippet']['resourceId']['videoId'])

        except KeyError:

            # If there are no next pages we need to check if this is not the first page before we append anything
            for song in response.json()['items']:
                songs_data.append(song['snippet']['resourceId']['videoId'])

        self.request_status(response)
        return songs_data

    def clone_playlist(self, source_id):
        """Clones any playlist from YouTube to your account"""

        # Creates an empty playlist in your account and retrieves its ID
        target_id = self.create_playlist('Cloned playlist')

        # Adds every video to the new playlist
        to_be_added = self.retrieve_videos_from_playlist(source_id)
        for video in to_be_added:
            self.add_video_to_playlist(target_id, video)

    def merge_playlists(self, first_playlist_id, second_playlist_id):
        """Merges 2 playlists. The second playlist will be deleted after this operation."""

        to_be_merged = self.retrieve_videos_from_playlist(second_playlist_id)

        for video in to_be_merged:
            self.add_video_to_playlist(first_playlist_id, video)

        self.delete_playlist(second_playlist_id)

    def top_three_videos_from_playlist(self, playlist_id):
        """Retrieves the top 3 videos by views from a specified playlist"""

        video_statistics = []
        video_ids = self.retrieve_videos_from_playlist(playlist_id)

        for video_id in video_ids:
            params = dict(
                part='snippet, statistics',
                id=video_id
            )
            response = requests.get(
                url=self._build_resource('videos'),
                params=params,
                headers=self.headers
            )
            for video in response.json()['items']:
                video_statistics.append([str(video['snippet']['title']), int(video['statistics']['viewCount'])])

        result = []

        for i in range(min(3, len(video_statistics))):
            result.append(video_statistics[i][0])

        return result

    def search(self, resource, resource_type='channel'):
        """Search for a video, a playlist or a channel resource (or maybe combined)"""

        params = dict(
            part='snippet',
            maxResults=20,
            type=resource_type,
            q=resource
        )

        response = requests.get(
            url=self._build_resource('search'),
            params=params,
            headers=self.headers
        )

        return response.json()
