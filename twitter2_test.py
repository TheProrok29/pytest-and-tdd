import pytest

from twitter import Twitter

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


@pytest.fixture(params=['list', 'backend'], name='twitter')
def fixture_twitter(backend, request):
    if request.param == 'list':
        twitter = Twitter()
    elif request.param == 'backend':
        twitter = Twitter(backend=backend)
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


def test_twitter_single_message(twitter):
    twitter.tweet("Test message")
    twitter.tweets == ["Test message"]


def test_twitter_long_message(twitter):
    with pytest.raises(Exception):
        twitter.tweet("test" * 41)
    assert twitter.tweets == []


@pytest.mark.parametrize("message, expected", (
        ("Test  #first message", ["first"]),
        ("#first Test message", ["first"]),
        ("#FIRST Test message", ["first"]),
        ("Test message #first", ["first"]),
        ("Test message #first #second", ["first", "second"])
))
def test_tweet_with_hashtag(twitter, message, expected):
    assert twitter.find_hashtags(message) == expected


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
