import requests
from lxml import objectify
from gi.repository import GdkPixbuf

USER_ID_URL = "http://www.ragechill.com/radio/getUserID"
SONG_GET_URL = "http://www.ragechill.com/radio/getSong"
REPOSITORY_URL = "https://s3.amazonaws.com/ragechill/%s"
SONG_INFO_URL = "http://www.ragechill.com/backend/getModal/"


class RageChill:

    def __init__(self):
        self.user_id = self.get_user()

    def get_user(self):
        r = requests.get(USER_ID_URL)
        if r.status_code is 200:
            user = objectify.fromstring(r.text.encode("UTF-8"))
            return user.userID
        else:
            raise CommunicationException(r.status_code)

    def get_song(self, rageLevel=2.5, curSong=0):
        payload = {'userID': self.user_id,
                   'rageLevel': rageLevel,
                   'curSong': curSong,
                   'web': 'true'}
        r = requests.get(SONG_GET_URL, params=payload)
        if r.status_code is 200:
            song_xml = objectify.fromstring(r.text.encode("UTF-8"))
            return song_xml.song

    def get_song_info(self, postID=0, songID=0):
        payload = {'postID': postID,
                   'songID': songID,
                   'web': 'true'}
        r = requests.get(SONG_INFO_URL, params=payload)
        if r.status_code is 200:
            song_xml = objectify.fromstring(r.text.encode("UTF-8"))
            return song_xml

    def get_song_stream(self, song_id=None):
        url = None
        if song_id is None:
            url = None
        else:
            mp3str = "%d.mp3" % song_id
            url = REPOSITORY_URL % mp3str
        return url

    def get_image_url(self, image=None):
        url = None
        if image is None:
            url = None
        else:
            url = REPOSITORY_URL % image
        return url

    def get_image_pixbuf(self, image=None):
        url = self.get_image_url(image)
        r = requests.get(url)
        loader = GdkPixbuf.PixbufLoader()
        loader.write(r.content)
        loader.close()
        return loader.get_pixbuf()


class CommunicationException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
