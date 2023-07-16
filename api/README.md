# Blogy API

---

- pagination
- auth - user
- posts - CRUD - Searching - md support - comment tag

## Documentation

### Users resource

- `GET /user/me` - gets current users info

  - requires **header** `jwt token`

- `POST /user` - create new user

  - requires **body** with `email, full_name, password, profile_pic(optional)`
  - requires **header** `jwt token`

- `PUT /user/me` - update current user

  - with optional **body** with `email, full_name, password, profile_pic`
  - requires **header** `jwt token`

- `DELETE /user/me` - delete current user

  - requires **header** `jwt token`

- `POST /user/login` - returns token
  - requires **body** with `email & password`

### Posts resource

- `GET /post` - gets all posts
- `GET /post/<slug>` - get single post with `slug`
- `GET /post/me` - gets all posts by current logged in user.

  - requires **`jwt token`**

- `POST /post` - create new post

  - requires **body** with `title, body, cover_pic(optional), is_published(optional) and tags(optional)`

  - requires **`jwt token`**

- `PUT /user/me` - update a post

  - with optional **body** with `title, body, cover_pic(optional), is_published(optional) and tags(optional)`
  - requires **`jwt token`**

- `DELETE /post/<slug>` - delete a post

  - requires **`jwt token`**

- `PUT /post/<slug>/publish` - publish a post

  - requires **`jwt token`**

- `PUT /post/<slug>/unpublish` - unpublish a post

  - requires **`jwt token`**

- `POST /post/<slug>/comment` - comment on a post

  - requires **`jwt token`**

- `GET /post/<slug>/comment` - get a comment on a post
