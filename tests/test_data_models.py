import praw
from pprint import pprint

from reddit_detective.data_models import Authored, CommentData, Submission, Subreddit, Redditor
from tests import api_


def test_subreddit():
    sub = Subreddit(api_, "learnpython", limit=100)
    assert sub.data["created_utc"]
    assert sub.main_type in sub.types
    assert sub.properties["created_utc"]
    assert sub.submissions() is not None


def test_submission():
    sub = Submission(api_, "jhd0px", limit=100)
    assert sub.data["created_utc"]
    assert sub.main_type in sub.types
    assert sub.properties["created_utc"]
    assert sub.comments() is not None
    assert isinstance(sub.author, Redditor)


def test_redditor():
    red = Redditor(api_, "Anub_Rekhan", limit=100)
    assert red.data["created_utc"]
    assert red.main_type in red.types
    assert red.properties["created_utc"]
    assert red.submissions() is not None
    assert red.comments() is not None


def test_commentdata():
    cd = CommentData(api_, "ga5umu3")
    assert cd.properties["text"]
    assert isinstance(cd.author, Redditor)
    assert isinstance(cd.submission, Submission)
    assert isinstance(cd.subreddit, Subreddit)
    assert cd.replies() is not None


def test_cypher_codes_node():
    sub = Subreddit(api_, "learnpython", limit=100)
    assert sub.types_code()
    assert sub.types[0] in sub.types_code()
    assert ":" in sub.types_code()
    assert sub.props_code()
    assert sub.properties["id"] in sub.props_code()
    assert ":" in sub.props_code()
    assert "{" in sub.props_code() and "}" in sub.props_code()
    assert sub.merge_node_code()
    assert "MERGE" in sub.merge_node_code()
    assert sub.types_code() in sub.merge_node_code()
    assert sub.props_code() in sub.merge_node_code()


def test_cypher_codes_rel():
    sub = Submission(api_, "hfulq4", limit=100)
    red = Redditor(api_, "Anub_Rekhan", limit=100)
    auth = Authored(api_, red, sub, sub.properties)
    assert auth.rel_type == "AUTHORED"
    assert auth.left_node.code() in auth.merge_code()
    assert auth.rel_type in auth.merge_code()
    assert auth.right_node.code() in auth.merge_code()


def run():
    test_subreddit()
    test_submission()
    test_redditor()
    test_cypher_codes_node()
    test_cypher_codes_rel()
