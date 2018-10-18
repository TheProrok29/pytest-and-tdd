from unittest.mock import patch, Mock, MagicMock

import pytest
import requests
from urllib3 import request

from twitter import Twitter


class ResponseGetMock(object):
    def json(self):
        return {'avatar_url': 'test'}


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr('requests.sessions.Session.request')


'''
#Niebezpieczna praktyka otwierania pliku przed każdym 
#z testów nawet jeśli nie jest to konieczne

@pytest.fixture(autouse=True)
def prepare_backend_file():
    with open('test.txt', 'w'):
        pass
'''


@pytest.fixture
def backend(tmpdir):
    temp_file = tmpdir.join('test.txt')
    temp_file.write('')
    return temp_file


@pytest.fixture(params=[None, 'TheProrok29'])
def username(request):
    return request.param


@pytest.fixture(params=['list', 'backend'], name='twitter')
def fixture_twitter(backend, username, request, monkeypatch):
    if request.param == 'list':
        twitter = Twitter(username=username)
    elif request.param == 'backend':
        twitter = Twitter(backend=backend, username=username)

    return twitter


'''@pytest.fixture
def twitter(request):
    twitter = Twitter()

    def fin():
        twitter.delete()

    request.addfinalizer(fin)
    return twitter
'''


def test_twitter_initialization(twitter):
    assert twitter


@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_twitter_single_message(avatar_mock, twitter):
    twitter.tweet("Test message")
    assert twitter.tweet_messages == ["Test message"]


def test_twitter_long_message(twitter):
    with pytest.raises(Exception):
        twitter.tweet("test" * 41)
    assert twitter.tweet_messages == []


@pytest.mark.parametrize("message, expected", (
        ("Test  #first message", ["first"]),
        ("#first Test message", ["first"]),
        ("#FIRST Test message", ["first"]),
        ("Test message #first", ["first"]),
        ("Test message #first #second", ["first", "second"])
))
def test_tweet_with_hashtag(twitter, message, expected):
    assert twitter.find_hashtags(message) == expected


def test_initialize_two_twitter_classes(backend):
    twitter1 = Twitter(backend=backend)
    twitter2 = Twitter(backend=backend)

    twitter1.tweet('Test1')
    twitter1.tweet('Test2')

    assert twitter2.tweet_messages == ['Test1', 'Test2']


'''
def test_tweet_with_hashtag():
    twitter = Twitter()
    message = "Test  #first message"
    assert "first" in twitter.find_hashtags(message)

def test_tweet_with_hashtag_on_beggining():
    twitter = Twitter()
    message = "#first Test message"
    assert "first" in twitter.find_hashtags(message)

def test_tweet_with_hashtag_uppercase():
    twitter = Twitter()
    message = "#FIRST Test message"
    assert "FIRST" in twitter.find_hashtags(message)

'''


@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_with_username(avatar_mock, twitter):
    if not twitter.username:
        pytest.skip()

    twitter.tweet('Test message')
    assert twitter.tweets == [{'message': 'Test message', 'avatar': 'test', 'hashtags': []}]
    avatar_mock.assert_called()


@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_with_hashtag_mock(avatar_mock, twitter):
    twitter.find_hashtags = Mock()
    twitter.find_hashtags.return_value = ['first']
    twitter.tweet('Test #second')
    assert twitter.tweets[0]['hashtags'] == ['first']
    twitter.find_hashtags.assert_called_with('Test #second')


'''
# Mock nie wspiera nadpisywania magicznych metod pythona

def test_twitter_version(twitter):
    twitter.version = Mock()
    twitter.version.__eq__.return_value = '2.0'
    assert twitter.version == '2.0'

'''


def test_twitter_version(twitter):
    twitter.version = Magic
    Mock()
    twitter.version.__eq__.return_value = '2.0'
    assert twitter.version == '2.0'
