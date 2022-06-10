import pytest
from app import schemas

#?? on the URL
def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostVotes(**post)

    posts_map = map(validate, res.json())
    #Can write more assert statements bases on this list but remember to order it
    posts_list = list(posts_map)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == 401

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostVotes(**res.json())
    assert post.Post.id == test_posts[0].id


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client):
    res = authorized_client.get(f"/posts/888888")
    assert res.status_code == 404

@pytest.mark.parametrize("title, content, published",[
    ("Awesome new title", "Awesome new content", True),
    ("Favorite pizza", "None", True),
    ("Tea or Coffee", "Tea", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):

    res = authorized_client.post("/posts/", json={"title":title, "content":content, "published":published})

    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client, test_user, test_posts):

    res = authorized_client.post("/posts/", json={"title":"title4", "content":"content4"})

    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == "title4"
    assert created_post.content == "content4"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client):
    res = client.post("/posts/", json={"title":"title4", "content":"content4"})

    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_authorized_user_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204

def test_authorized_user_delete_post_nonexist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/999999")

    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[4].id}")

    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = schemas.PostResponse(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "id": test_posts[4].id
    }
    res = authorized_client.put(f"/posts/{test_posts[4].id}", json=data)

    assert res.status_code == 403

def test_authorized_user_update_post_nonexist(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "id": test_posts[4].id
    }
    
    res = authorized_client.put(f"/posts/999999", json=data)

    assert res.status_code == 404

def test_update_other_user_post(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "id": test_posts[4].id
    }
    
    res = authorized_client.put(f"/posts/{test_posts[4].id}", json=data)

    assert res.status_code == 403