# karena melihat post hrs login maka gunakan fixture authorized_client yg dibuat pd conftest.py
# def test_get_all_posts(authorized_client):
#     res = authorized_client.get('/posts/myposts')
#     print(res.json())
#     assert res.status_code == 200

# # simpan data dan lihat datanya
# def test_get_all_posts(authorized_client, test_posts):
#     res = authorized_client.get('/posts/myposts')
#     print(res.json())
#     assert res.status_code == 200

from app import schema
import pytest

def test_get_all_myposts(authorized_client, test_posts):
    res = authorized_client.get('/posts/myposts')
    # debug data post dari database
    # print("="*50)
    # print([data for data in test_posts])

    def validate(post):
        return schema.PostResponse(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    # debug data yg ditampilkan
    # print("="*50)
    # print(posts_list[0].id)
    
    assert len(res.json()) == len(test_posts) 
    assert res.status_code == 200
    # cek id data yg ditampilkan dg data di database
    assert posts_list[0].id == test_posts[0].id

# test tanpa login get all mypost
def test_unauthorized_get_all_myposts(client, test_posts):
    res = client.get('/posts/myposts')
    assert res.status_code == 401

# test tanpa login get 1 mypost
def test_unauthorized_get_one_mypost(client, test_posts):
    res = client.get(f'/posts/mypost/{test_posts[0].id}')
    assert res.status_code == 401

# get 1 mypost not exist
def test_get_one_mypost_no_exist(authorized_client):
    res = authorized_client.get('/posts/mypost/99999')
    assert res.status_code == 404
 
def test_get_one_mypost(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/mypost/{test_posts[0].id}')
    data = schema.PostOut(**res.json())
    assert data.Post.id == test_posts[0].id
    assert data.Post.nama == test_posts[0].nama
    # karena vote ada di tabel vote maka pd test_posts tdk ada vote tp untuk data.votes itu ada
    # assert data.votes == test_posts[0].vote

@pytest.mark.parametrize("nama, umur, alamat, published",[
    ("john", 70, "alam semesta", False),
    ("bumi", 100, "like earth", True),
])
def test_create_post(authorized_client, test_user, test_posts,nama, umur, alamat, published):
    res = authorized_client.post("/posts/createnew", json={"nama":nama, "umur":umur, "alamat":alamat,"published":published})
    create_post = schema.PostResponse(**res.json())
    assert res.status_code == 201
    assert create_post.nama == nama
    assert create_post.umur == umur
    assert create_post.alamat == alamat
    assert create_post.published == published
    assert create_post.owner_id == test_user['id']

def test_create_post_default_published(authorized_client, test_user,test_posts):
    res = authorized_client.post("/posts/createnew", json={"nama":"nama", "umur":10, "alamat":"alamat"})
    create_post = schema.PostResponse(**res.json())
    assert res.status_code == 201
    assert create_post.nama == "nama"
    assert create_post.umur == 10
    assert create_post.alamat == "alamat"
    assert create_post.published == True
    assert create_post.owner_id == test_user['id']

# test tanpa login get all mypost
def test_unauthorized_create_post(client, test_posts):
    res = client.post("/posts/createnew", json={"nama":"nama", "umur":10, "alamat":"alamat"})
    assert res.status_code == 401

# test tanpa login hapus post tertentu
def test_unauthorized_delete_post(client, test_posts):
    res = client.delete(f"/posts/delete/{test_posts[0].id}")
    assert res.status_code == 401

def test_post(authorized_client, test_user,test_posts):
    res = authorized_client.delete(f"/posts/delete/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client, test_user,test_posts):
    res = authorized_client.delete(f"/posts/delete/9999999")
    assert res.status_code == 404

# hapus post dengan akun yg tdk sehrsnya/akun lain
def test_delete_post_other_account(authorized_client, test_user,test_posts2):
    # post dg id 5 itu hanya bisa dilakukan oleh user 2
    res = authorized_client.delete(f"/posts/delete/{test_posts2[5].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user,test_posts):
    data = {
        "nama":"update nama",
        "umur":9999,
        "alamat":"update alamat",
        "published": False
    }
    res = authorized_client.put(f"/posts/update/{test_posts[0].id}", json=data)
    update_post = schema.PostResponse(**res.json())
    assert res.status_code == 200
    assert update_post.nama == data['nama']
    assert update_post.umur == data["umur"]
    assert update_post.alamat == data["alamat"]
    assert update_post.published == data["published"]

def test_update_post_other_account(authorized_client, test_user,test_posts2):
    data = {
        "nama":"update nama",
        "umur":9999,
        "alamat":"update alamat",
        "published": False,
        # "id":test_posts2[5].id
    }
    res = authorized_client.put(f"/posts/update/{test_posts2[5].id}", json=data)
    assert res.status_code == 403

def test_update_post_unauthorized(client, test_user,test_posts):
    res = client.put(f"/posts/update/{test_posts[0].id}")
    assert res.status_code == 401

def test_update_post_no_exist(authorized_client, test_user,test_posts):
    data = {
        "nama":"update nama",
        "umur":9999,
        "alamat":"update alamat",
        "published": False,
        # "id":test_posts2[5].id
    }
    res = authorized_client.put(f"/posts/update/10000", json=data)
    assert res.status_code == 404