from youtube_access import *


if __name__ == '__main__':

    # authenticate to YouTube
    yt = YouTube()
    yt.authenticate()

    # GET requests
    yt.my_playlists()
    yt.retrieve_playlist_details('PL-dhKbEXN9kMWeGTJGuEvuSXSkK7612bI')
    yt.retrieve_videos_from_playlist('PL-dhKbEXN9kMWeGTJGuEvuSXSkK7612bI')
    yt.top_three_videos('PL-dhKbEXN9kMWeGTJGuEvuSXSkK7612bI')
    yt.top_three_videos()
    yt.search('cars', 'video')

    # POST requests
    yt.create_playlist('random playlist')
    yt.add_video_to_playlist('PL-dhKbEXN9kMWeGTJGuEvuSXSkK7612bI', 'F5mRW0jo-U4')
    yt.clone_playlist('PLdN7Dwi6JGXuMewNdWRg7yA7ueQ35OSaY')
    yt.merge_playlists('PL-dhKbEXN9kMWeGTJGuEvuSXSkK7612b', 'PL-dhKbEXN9kO9aK5xQ2zsz-6WmNI4Wp48')

    # PUT requests
    yt.edit_playlist_details('PL-dhKbEXN9kMWeGTJGuEvuSXSkK7612bI', new_title='My awesome playlist')

    # DELETE requests
    # yt.remove_video_from_playlist('') -> need a video ID for that
    yt.delete_playlist('PL-dhKbEXN9kMgfawOoKTswppkViUXNVVN')

    # playlist.create('a')
    # playlist.clone('PLKe-Zuux9p9vWWUVGyY5SPMO6MpRDjZ5x')
    # playlist.top_three_videos('PL-dhKbEXN9kMWeGTJGuEvuSXSkK7612bI')
    # yt.my_playlists()
    # yt.retrieve_videos_from_playlist('PL-dhKbEXN9kMWeGTJGuEvuSXSkK7612bI')
    yt.top_three_videos_from_playlist()