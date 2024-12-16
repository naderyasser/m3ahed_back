## **API Documentation: M3ahed**

### **Endpoint:**

```
GET /api/posts
```

### **Description:**

This endpoint allows clients to fetch posts, with optional filtering by category, searching by title or content, and sorting by different attributes. It supports pagination for efficient data retrieval.

---

### **Query Parameters:**

| Parameter  | Type                 | Description                                                                                                   |
| ---------- | -------------------- | ------------------------------------------------------------------------------------------------------------- |
| `category` | `string` (optional)  | Filter posts by category. If not provided, returns all posts.                                                 |
| `search`   | `string` (optional)  | Search term to search in both title and content.                                                              |
| `page`     | `integer` (optional) | The page number for pagination. Default is `1`.                                                               |
| `limit`    | `integer` (optional) | Number of items per page. Default is `10`.                                                                    |
| `sort_by`  | `string` (optional)  | The field by which to sort the results. Default is `created_at`. Possible values: `created_at`, `views`, etc. |
| `order`    | `string` (optional)  | The order of sorting. Default is `desc`. Possible values: `asc`, `desc`.                                      |

---

### **Response:**

The response includes metadata for pagination and the list of posts matching the request criteria.

#### **Response Fields:**

| Field         | Type      | Description                                  |
| ------------- | --------- | -------------------------------------------- |
| `total_items` | `integer` | Total number of posts that match the filter. |
| `page`        | `integer` | Current page number.                         |
| `limit`       | `integer` | Number of items per page.                    |
| `total_pages` | `integer` | Total number of pages available.             |
| `posts`       | `array`   | List of post objects.                        |

#### **Post Object Fields:**

| Field        | Type      | Description                                                      |
| ------------ | --------- | ---------------------------------------------------------------- |
| `id`         | `integer` | The unique ID of the post.                                       |
| `title`      | `string`  | The title of the post.                                           |
| `category`   | `string`  | The category of the post.                                        |
| `content`    | `string`  | The content of the post.                                         |
| `banner_url` | `string`  | The URL of the banner image associated with the post.            |
| `views`      | `integer` | The number of views the post has received.                       |
| `status`     | `string`  | The publication status of the post (e.g., `published`, `draft`). |
| `created_at` | `string`  | The creation date of the post (ISO 8601 format).                 |
| `updated_at` | `string`  | The last update date of the post (ISO 8601 format).              |
| `media`      | `array`   | A list of media objects associated with the post.                |

#### **Media Object Fields:**

| Field        | Type      | Description                                              |
| ------------ | --------- | -------------------------------------------------------- |
| `id`         | `integer` | The unique ID of the media.                              |
| `name`       | `string`  | The name of the media file.                              |
| `media_type` | `string`  | The type of media (e.g., `image`, `video`).              |
| `url`        | `string`  | The URL of the media file.                               |
| `status`     | `string`  | The publication status of the media (e.g., `published`). |
| `created_at` | `string`  | The creation date of the media file (ISO 8601 format).   |

---

### **Example Request 1: Fetch All Posts**

This request fetches all posts without any filters.

```
GET /posts
```

#### **Query Parameters:**

```json
{
  "page": 1,
  "limit": 10
}
```

#### **Example Response:**

```json
{
  "total_items": 25,
  "page": 1,
  "limit": 10,
  "total_pages": 3,
  "posts": [
    {
      "id": 1,
      "title": "Example Post",
      "category": "news",
      "content": "This is a sample post.",
      "banner_url": "http://localhost:5000/uploads/banner_image.jpg",
      "views": 123,
      "status": "published",
      "created_at": "2024-12-02T12:00:00",
      "updated_at": "2024-12-02T12:00:00",
      "media": [
        {
          "id": 1,
          "name": "example_image.jpg",
          "media_type": "image",
          "url": "http://localhost:5000/uploads/example_image.jpg",
          "status": "published",
          "created_at": "2024-12-02T12:00:00"
        }
      ]
    }
  ]
}
```

---

### **Example Request 2: Fetch Posts by Category**

This request fetches all posts in the `news` category.

```
GET /posts?category=news
```

#### **Query Parameters:**

```json
{
  "page": 1,
  "limit": 5,
  "category": "news"
}
```

#### **Example Response:**

```json
{
  "total_items": 5,
  "page": 1,
  "limit": 5,
  "total_pages": 1,
  "posts": [
    {
      "id": 1,
      "title": "Breaking News",
      "category": "news",
      "content": "This is an urgent update.",
      "banner_url": "http://localhost:5000/uploads/banner_news.jpg",
      "views": 100,
      "status": "published",
      "created_at": "2024-12-02T12:00:00",
      "updated_at": "2024-12-02T12:00:00",
      "media": [
        {
          "id": 1,
          "name": "news_image.jpg",
          "media_type": "image",
          "url": "http://localhost:5000/uploads/news_image.jpg",
          "status": "published",
          "created_at": "2024-12-02T12:00:00"
        }
      ]
    }
  ]
}
```

---

### **Example Request 3: Search Posts by Title or Content**

This request searches for posts containing the word "example".

```
GET /posts?search=example
```

#### **Query Parameters:**

```json
{
  "page": 1,
  "limit": 10,
  "search": "example"
}
```

#### **Example Response:**

```json
{
  "total_items": 2,
  "page": 1,
  "limit": 10,
  "total_pages": 1,
  "posts": [
    {
      "id": 1,
      "title": "Example Post",
      "category": "news",
      "content": "This is a sample post containing the word example.",
      "banner_url": "http://localhost:5000/uploads/example_banner.jpg",
      "views": 150,
      "status": "published",
      "created_at": "2024-12-01T12:00:00",
      "updated_at": "2024-12-01T12:00:00",
      "media": []
    }
  ]
}
```

---

### **Error Responses:**

#### **400 Bad Request:**

If the query parameters are incorrect or invalid:

```json
{
  "error": "Invalid request. Please check the query parameters."
}
```

---

### **Notes:**

- If no category is provided, all posts will be returned.
- If no search term is provided, it will return posts based on other filters (e.g., category, pagination).
- The `media` field is an array, even if there is only one media file associated with the post.
- The `created_at` and `updated_at` fields are formatted in ISO 8601 date-time format.

---



{
	"info": {
		"_postman_id": "9fae8b04-57d7-4823-bdee-bd0b828fa2f4",
		"name": "Ma3ahed",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
		"_exporter_id": "40382157",
		"_collection_link": "https://m3ahed.postman.co/workspace/c8ac6afb-f3d9-41c1-abfc-a661665b7afe/collection/40382157-9fae8b04-57d7-4823-bdee-bd0b828fa2f4?action=share&source=collection_link&creator=40382157"
	},
	"item": [
		{
			"name": "Fetch Post by title or content",
			"event": [
				{
					"listen": "test",
					"script": {
						"exec": [
							""
						],
						"type": "text/javascript",
						"packages": {}
					}
				}
			],
			"protocolProfileBehavior": {
				"followRedirects": true,
				"disableUrlEncoding": false,
				"disableCookies": false
			},
			"request": {
				"method": "GET",
				"header": [
					{
						"key": "User-Agent",
						"value": "insomnia/10.2.0",
						"disabled": true
					}
				],
				"url": {
					"raw": "http://127.0.0.1:5000/api/posts?search=example",
					"protocol": "http",
					"host": [
						"127",
						"0",
						"0",
						"1"
					],
					"port": "5000",
					"path": [
						"api",
						"posts"
					],
					"query": [
						{
							"key": "search",
							"value": "example"
						}
					]
				}
			},
			"response": []
		},
		{
			"name": "Fetch Post by category",
			"event": [
				{
					"listen": "test",
					"script": {
						"exec": [
							""
						],
						"type": "text/javascript",
						"packages": {}
					}
				}
			],
			"protocolProfileBehavior": {
				"followRedirects": true,
				"disableUrlEncoding": false,
				"disableCookies": false
			},
			"request": {
				"method": "GET",
				"header": [
					{
						"key": "User-Agent",
						"value": "insomnia/10.2.0",
						"disabled": true
					}
				],
				"url": {
					"raw": "http://127.0.0.1:5000/api/posts?category=news",
					"protocol": "http",
					"host": [
						"127",
						"0",
						"0",
						"1"
					],
					"port": "5000",
					"path": [
						"api",
						"posts"
					],
					"query": [
						{
							"key": "category",
							"value": "news"
						}
					]
				}
			},
			"response": []
		},
		{
			"name": "Get Posts",
			"event": [
				{
					"listen": "test",
					"script": {
						"exec": [
							""
						],
						"type": "text/javascript",
						"packages": {}
					}
				}
			],
			"protocolProfileBehavior": {
				"followRedirects": true,
				"disableUrlEncoding": false,
				"disableCookies": false
			},
			"request": {
				"method": "GET",
				"header": [
					{
						"key": "User-Agent",
						"value": "insomnia/10.2.0",
						"disabled": true
					}
				],
				"url": {
					"raw": "http://127.0.0.1:5000/api/posts",
					"protocol": "http",
					"host": [
						"127",
						"0",
						"0",
						"1"
					],
					"port": "5000",
					"path": [
						"api",
						"posts"
					]
				}
			},
			"response": []
		},
		{
			"name": "Get a post",
			"request": {
				"method": "GET",
				"header": [],
				"url": {
					"raw": "http://127.0.0.1:5000/api/post/1",
					"protocol": "http",
					"host": [
						"127",
						"0",
						"0",
						"1"
					],
					"port": "5000",
					"path": [
						"api",
						"post",
						"1"
					]
				}
			},
			"response": []
		},
		{
			"name": "Post a post",
			"request": {
				"auth": {
					"type": "jwt",
					"jwt": [
						{
							"key": "algorithm",
							"value": "HS256",
							"type": "string"
						},
						{
							"key": "isSecretBase64Encoded",
							"value": false,
							"type": "boolean"
						},
						{
							"key": "payload",
							"value": "{}",
							"type": "string"
						},
						{
							"key": "addTokenTo",
							"value": "header",
							"type": "string"
						},
						{
							"key": "headerPrefix",
							"value": "Bearer",
							"type": "string"
						},
						{
							"key": "queryParamKey",
							"value": "token",
							"type": "string"
						},
						{
							"key": "header",
							"value": "{}",
							"type": "string"
						}
					]
				},
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "{\r\n    \"title\": \"Test\",\r\n    \"category\": \"category\",\r\n    \"content\": \"content\",\r\n    \"banner_url\": \"banner_url\",\r\n    \"status\": \"draft\"\r\n}",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "http://127.0.0.1:5000/api/posts",
					"protocol": "http",
					"host": [
						"127",
						"0",
						"0",
						"1"
					],
					"port": "5000",
					"path": [
						"api",
						"posts"
					]
				}
			},
			"response": []
		},
		{
			"name": "Login",
			"request": {
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "{\r\n    \"username\": \"username\",\r\n    \"password\": \"password\"\r\n}",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "http://127.0.0.1:5000/api/login",
					"protocol": "http",
					"host": [
						"127",
						"0",
						"0",
						"1"
					],
					"port": "5000",
					"path": [
						"api",
						"login"
					]
				}
			},
			"response": []
		},
		{
			"name": "Put a post",
			"request": {
				"method": "PUT",
				"header": [],
				"url": {
					"raw": "http://127.0.0.1:5000/api/posts/1",
					"protocol": "http",
					"host": [
						"127",
						"0",
						"0",
						"1"
					],
					"port": "5000",
					"path": [
						"api",
						"posts",
						"1"
					]
				}
			},
			"response": []
		},
		{
			"name": "Delete a post",
			"request": {
				"method": "DELETE",
				"header": [],
				"url": {
					"raw": "http://127.0.0.1:5000/api/post/1",
					"protocol": "http",
					"host": [
						"127",
						"0",
						"0",
						"1"
					],
					"port": "5000",
					"path": [
						"api",
						"post",
						"1"
					]
				}
			},
			"response": []
		},
		{
			"name": "Post a media",
			"request": {
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "{\r\n    \"media_type\": \"jpg\"\r\n}",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "http://127.0.0.1:5000/api/post/1/media",
					"protocol": "http",
					"host": [
						"127",
						"0",
						"0",
						"1"
					],
					"port": "5000",
					"path": [
						"api",
						"post",
						"1",
						"media"
					]
				}
			},
			"response": []
		},
		{
			"name": "Delete media",
			"request": {
				"method": "DELETE",
				"header": [],
				"url": {
					"raw": "http://127.0.0.1:5000/api/media/1",
					"protocol": "http",
					"host": [
						"127",
						"0",
						"0",
						"1"
					],
					"port": "5000",
					"path": [
						"api",
						"media",
						"1"
					]
				}
			},
			"response": []
		}
	]
}
