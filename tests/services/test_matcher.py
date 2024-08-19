import pytest

from app.models import Content, Interest, Tag, User
from app.services.matcher import match_users_to_content


@pytest.fixture
def sample_user():
    user = User(name="John Dow")
    user.interests = [
        Interest(type="instrument", value="VOD.L", threshold=0.5),
        Interest(type="country", value="UK", threshold=0.24),
    ]
    return user


@pytest.fixture
def sample_content():
    content = Content(id="123", title="UK Market News", content="Some content about UK.")
    content.tags = [Tag(type="country", value="UK", threshold=0.25)]
    return content


def test_match_users_to_content_with_match(sample_user, sample_content):
    users = [sample_user]
    content = [sample_content]

    result = match_users_to_content(users, content)

    assert len(result) == 1
    assert "John Dow" in result
    assert len(result["John Dow"]) == 1
    assert result["John Dow"][0] == sample_content


def test_match_users_to_content_no_match():
    user = User(name="Alice")
    user.interests = [Interest(type="instrument", value="AAPL", threshold=0.7)]

    content = Content(id="456", title="Tech News", content="Some tech content")
    content.tags = [Tag(type="sector", value="Technology", threshold=0.8)]

    result = match_users_to_content([user], [content])

    assert len(result) == 1
    assert "Alice" in result
    assert len(result["Alice"]) == 0


def test_match_users_to_content_multiple_users_and_content(sample_user, sample_content):
    user2 = User(name="Bob")
    user2.interests = [Interest(type="sector", value="Finance", threshold=0.3)]

    content2 = Content(id="789", title="Finance News", content="Some finance content")
    content2.tags = [Tag(type="sector", value="Finance", threshold=0.5)]

    users = [sample_user, user2]
    content = [sample_content, content2]

    result = match_users_to_content(users, content)

    assert len(result) == 2
    assert "John Dow" in result
    assert "Bob" in result
    assert len(result["John Dow"]) == 1
    assert result["John Dow"][0] == sample_content
    assert len(result["Bob"]) == 1
    assert result["Bob"][0] == content2


def test_match_users_to_content_threshold_edge_case(sample_user, sample_content):
    # Modify the user's interest threshold to be exactly equal to the content's tag threshold
    sample_user.interests[1].threshold = 0.25

    result = match_users_to_content([sample_user], [sample_content])

    assert len(result) == 1
    assert "John Dow" in result
    assert len(result["John Dow"]) == 1
    assert result["John Dow"][0] == sample_content


def test_match_users_to_content_empty_inputs():
    result = match_users_to_content([], [])

    assert isinstance(result, dict)
    assert len(result) == 0


def test_match_users_to_content_multiple_users_and_content_complex():
    # Create multiple users
    user1 = User(name="Alice")
    user1.interests = [
        Interest(type="country", value="US", threshold=0.3),
        Interest(type="sector", value="Technology", threshold=0.5),
    ]

    user2 = User(name="Bob")
    user2.interests = [
        Interest(type="country", value="UK", threshold=0.2),
        Interest(type="instrument", value="AAPL", threshold=0.6),
    ]

    user3 = User(name="Charlie")
    user3.interests = [
        Interest(type="sector", value="Finance", threshold=0.4),
        Interest(type="country", value="Germany", threshold=0.3),
    ]

    # Create multiple content pieces
    content1 = Content(id="001", title="US Tech News", content="Content about US tech")
    content1.tags = [
        Tag(type="country", value="US", threshold=0.8),
        Tag(type="sector", value="Technology", threshold=0.9),
    ]

    content2 = Content(id="002", title="UK Market Update", content="Content about UK market")
    content2.tags = [Tag(type="country", value="UK", threshold=0.7), Tag(type="sector", value="Finance", threshold=0.5)]

    content3 = Content(id="003", title="Apple Stock News", content="Content about AAPL stock")
    content3.tags = [
        Tag(type="instrument", value="AAPL", threshold=0.9),
        Tag(type="country", value="US", threshold=0.4),
    ]

    content4 = Content(id="004", title="German Economy", content="Content about German economy")
    content4.tags = [
        Tag(type="country", value="Germany", threshold=0.6),
        Tag(type="sector", value="Economy", threshold=0.7),
    ]

    content5 = Content(id="005", title="German Companies", content="Content about German companies")
    content5.tags = [Tag(type="country", value="Germany", threshold=0.1)]

    users = [user1, user2, user3]
    content = [content1, content2, content3, content4, content5]

    result = match_users_to_content(users, content)

    # Assertions
    assert len(result) == 3
    assert "Alice" in result
    assert "Bob" in result
    assert "Charlie" in result

    # Check Alice's matches
    assert len(result["Alice"]) == 2
    assert content1 in result["Alice"]
    assert content3 in result["Alice"]

    # Check Bob's matches
    assert len(result["Bob"]) == 2
    assert content2 in result["Bob"]
    assert content3 in result["Bob"]

    # Check Charlie's matches
    assert len(result["Charlie"]) == 2
    assert content2 in result["Charlie"]
    assert content4 in result["Charlie"]
