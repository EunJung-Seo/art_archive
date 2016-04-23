# art_archive

### art_archive Database
- artists와 images 두 개의 테이블이 있다.
- 두 테이블 모두 Primary Key는 id이며 auto_increment이다.
- 두 테이블은 one to many 관계이다.
- artists 테이블의 column들은 다음과 같다.
  - name : varchar(45)
  - birth_year : int(11)
  - death_year : int(11)
  - country : varchar(45)
  - genre : varchar(45)
- images 테이블의 column들은 다음과 같다.
  - image_url : varchar(255)
  - title : varchar(255)
  - year : int(11)
  - artist_id : int(11), ``Foreign Key : artists 테이블의 id``
  - description : varchar(255)

> 현재 두 테이블은 one to many 관계이지만, artist_id 없이도 images 테이블에 image 추가가 가능하다. 

> 또한 모든 column이 ``null``인 artists row와 images row가 생성 가능하다.

> 유의미한 데이터를 위해 ``not null``을 지정할 필요가 있다. artists.name, images.artist_id, images.title column에 우선적으로 적용해야 한다.




####1) ‘제니 오델'이라는 artist의 image title들 가져오기
**query**
```
SELECT images.title 
FROM artists 
INNER JOIN images 
ON artists.id = images.artist_id 
WHERE artists.name = '제니 오델';
```
- ``INNER JOIN``을 사용하면 특정 작가와 그 작가의 작품을 한 row로 볼 수 있게 된다. 
- 이렇게 나온 row들에서 ``WHERE``를 사용하여 작가의 이름이 '제니 오델'인 image title을 가져온다.

**return**
```
+------------------+
| title            |
+------------------+
| 쓰레기 셀카         |
+------------------+
1 row in set (0.00 sec)
```

####2) ‘인상주의' artist의 image들 중 3개의 image 가져오기
**query**
```
SELECT images.*
FROM artists
INNER JOIN images
ON artists.id = images.artist_id
WHERE artists.genre = '인상주의'
LIMIT 3;
```
- ``INNER JOIN``을 사용하면 특정 작가와 그 작가의 작품을 한 row로 볼 수 있게 된다. 
- 이렇게 나온 row들에서 ``WHERE``를 사용하여 genre가 '인상주의'인 row들만 걸러낸다.
- ``LIMIT``의 count 갯수를 3으로 주어 3개의 이미지만 가져온다.

**return**
```
+----+----------------------------------------------------------------------------------------------------+----------------------------+------+-----------+---------------------+
| id | image_url                                                                                          | title                      | year | artist_id | description         |
+----+----------------------------------------------------------------------------------------------------+----------------------------+------+-----------+---------------------+
|  3 | http://www.gulbenkian.pt/prjdir/gulbenkian/images/mediaRep/museu/colecao/pintura/Inv._2361Trat.jpg | 비눗방울 부는 소년             | 1867 |       104 | 캔버스에 유채           |
| 46 | http://www.manet.org/images/gallery/the-luncheon-on-the-grass.jpg                                  | 풀밭 위의 점심식사             | 1863 |       104 | 캔버스에 유채           |
|  8 | http://mfas3.s3.amazonaws.com/objects/SC232880.jpg                                                 | 시골 경마장                  | 1869 |       109 | 캔버스에 유채           |
+----+----------------------------------------------------------------------------------------------------+----------------------------+------+-----------+---------------------+
3 rows in set (0.00 sec)
```


####3) images 테이블에 새로운 image 추가하기(query statement만)
현재 images 테이블은 id를 제외한 모든 column이 ``null``인 row를 만들 수 있다. 하지만 의미있는 정보를 추가한다는 가정 하에 아래와 같은 query로 image를 추가하였다. 여기서 '의미있는 정보'란 artists 테이블에 등록된 작가의 작품이고 title과 image_url이 있는 작품의 정보이다.

**query**
```
INSERT INTO images(image_url, title, year,artist_id,description) 
VALUES 
(
    "http://www.cha.go.kr/unisearch/images/national_treasure/1611691.jpg", 
    '금강전도',
    1734,
    (SELECT id FROM artists WHERE name='정선'),
    "종이에 수묵"
);
```
 


####4) 가장 많은 image들을 가진 artist 가져오기
**query**
```
SELECT artists.*, COUNT(images.id) AS number_of_images
FROM artists
INNER JOIN images
ON artists.id = images.artist_id
GROUP BY artists.id
ORDER BY number_of_images DESC
LIMIT 1;
```
- ``INNER JOIN``을 사용하면 특정 작가와 그 작가의 작품을 한 row로 볼 수 있게 된다. 
- 이렇게 나온 row들을 ``GROUP BY``를 사용하여 artist의 id를 기준으로 그룹화한다. 2개 이상의 작품을 가진 작가들은 중복이 제거되어 하나의 row로 표현된다.
- 중복이 제거되면 작품의 갯수를 헤아릴 수 없기 때문에 중복되는 row의 갯수를 세어 number_of_images로 표시한다.
- number_of_images의 갯수를 기준으로 내림차순 정렬 후(``ORDER BY``), ``LIMIT`` count를 1로 설정하여 가장 많은 image를 가진 artist 정보를 가져온다.  

**return**
```
+-----+----------------------+------------+------------+--------------+---------------------+------------------+
| id  | name                 | birth_year | death_year | country      | genre               | number_of_images |
+-----+----------------------+------------+------------+--------------+---------------------+------------------+
| 102 | 빈센트 반 고흐          |       1853 |       1890 | 네더란드       | 후기 인상주의           |                4 |
+-----+----------------------+------------+------------+--------------+---------------------+------------------+
1 row in set (0.00 sec)
```

### CRUD
Create, Read, Update, Delete의 약자이다. 데이터를 쓰고 읽고 수정하고 삭제하는 데이터 저장장치의 가장 기본적인 네 가지 기능이다. art_archive를 예로 들면,

- Create : artist 추가, image 추가
- Read : 조건에 맞는 정보 가져오기(1번, 2번, 4번 문제)
- Update : artist 이름 수정, image_url 변경, image description 추가 등
- Delete : artist 삭제, image 삭제

이 네 가지 기능을 사용해 데이터를 관리한다.


### art_archive API
#### 1) artists 목록

현재 저장되어 있는 artist들의 목록을 가져온다. parameter들을 활용하면 원하는 artists 목록을 가져올 수 있다.

* **URL**

  /artists

* **Method:**

  `GET` 
  
*  **URL Params**

   
   **Required:**
 
   None

   **Optional:**
 
   PARAMETER | TYPE | DESCRIPTION
   ------------ | ------------- | -------------
   name | string | 입력된 name과 일치하는 작가의 정보를 리턴한다.
   count |integer | 입력된 count 갯수만큼 목록을 보여준다.
   offset |integer | count와 함께 사용된다. 입력된 offset부터 count 갯수만큼 목록을 보여준다. 
   image_detail | 0 or 1 | 1일 경우 작가의 작품 정보도 포함한다. 기본은 0.

  


* **Data Params**

  None

* **Success Response:**
  
  GET ``/artists?name=빈센트 반 고흐``

  * **Code:** 200 <br />
    **Content:** <br />
    ```
    /*---------------------
    images_detail이 0인 경우
    ---------------------*/
    {
      "images_detail": 0,
      "list": [
        {
          "id": 102,
          "name": "빈센트 반 고흐",
          "birth_year": 1853,
          "death_year": 1890,
          "country": "네더란드",
          "genre": "후기 인상주의",
        },
        ...
      ]
    }


    /*---------------------
    images_detail이 1인 경우
    ---------------------*/
    {
      "images_detail": 1,
      "list": [
        {
          "id": 102,
          "name": "빈센트 반 고흐",
          "birth_year": 1853,
          "death_year": 1890,
          "country": "네더란드",
          "genre": "후기 인상주의",
          "images" : [
            {
              "id": 1,
              "image_url": "http://www.vggallery.com/painting/f_0467.jpg",
              "title": "밤의 카페 테라스",
              "year": 1888,
              "description": "캔버스에 유채",
            },
            ...
          ]
        },
        ...
      ]
    }
    ```
* **Error Response:**

  * **Code:** 400 Bad Request <br />
    **Content:** `{ error : "Invalid Request. Please check the syntax" }`

  OR

  * **Code:** 500 Internal Server Error <br />
    **Content:** `{ error : "Internal Server Error" }`


#### 2) images 목록

현재 저장되어 있는 image들의 목록을 가져온다. parameter들을 활용하면 원하는 image 목록을 가져올 수 있다.

* **URL**

  /images

* **Method:**

  `GET` 
  
*  **URL Params**

   
   **Required:**
 
   None

   **Optional:**
 
   PARAMETER | TYPE | DESCRIPTION
   ------------ | ------------- | -------------
   title | string | 입력된 title과 일치하는 image의 정보를 리턴한다.
   artist | string | 입력된 artist의 image 목록을 리턴한다.
   count |integer | 입력된 count 갯수만큼 목록을 보여준다.
   offset |integer | count와 함께 사용된다. 입력된 offset부터 count 갯수만큼 목록을 보여준다.

  


* **Data Params**

  None

* **Success Response:**
  
  GET ``/images?artist=빈센트 반 고흐``  

  * **Code:** 200 <br />
    **Content:** <br />
  ```
    {
      "list": [
        {
          "id": 1,
          "image_url": "http://www.vggallery.com/painting/f_0467.jpg",
          "title": "밤의 카페 테라스",
          "year": 1888,
          "description": "캔버스에 유채"
          "artist" : {
              "id": 102,
              "name": "빈센트 반 고흐",
              "birth_year": 1853,
              "death_year": 1890,
              "country": "네더란드",
              "genre": "후기 인상주의",
          },
        },
        ...
      ]
    }
  ```
* **Error Response:**

  * **Code:** 400 Bad Request <br />
    **Content:** `{ error : "Invalid Request. Please check the syntax" }`

  OR

  * **Code:** 500 Internal Server Error <br />
    **Content:** `{ error : "Internal Server Error" }`



#### 3) artist 보기

id가 일치하는 artist의 정보를 보여준다.

* **URL**

  /artist/id

* **Method:**

  `GET` 
  
*  **URL Params**

   
   **Required:**
 
   PARAMETER | TYPE | DESCRIPTION
   ------------ | ------------- | -------------
   id | integer | 보고자 하는 artist의 id


   **Optional:**
 
   PARAMETER | TYPE | DESCRIPTION
   ------------ | ------------- | -------------
   images_detail | 0 or 1 | 1일 경우 작가의 작품 정보도 포함한다. 기본은 0.

  


* **Data Params**

  None

* **Success Response:**
  
  GET ``/artist/102``  

  * **Code:** 200 <br />
    **Content:** <br />
  ```
    /*------------------
    images_detail이 0일 때
    -------------------*/
    {
      "images_detail": 0,
      "artist": {
          "id": 102,
          "name": "빈센트 반 고흐",
          "birth_year": 1853,
          "death_year": 1890,
          "country": "네더란드",
          "genre": "후기 인상주의",
        },
    }

    /*------------------
    images_detail이 1일 때
    -------------------*/
    {
      "images_detail": 1,
      "artist": {
          "id": 102,
          "name": "빈센트 반 고흐",
          "birth_year": 1853,
          "death_year": 1890,
          "country": "네더란드",
          "genre": "후기 인상주의",
          "images" : [
            {
              "id": 1,
              "image_url": "http://www.vggallery.com/painting/f_0467.jpg",
              "title": "밤의 카페 테라스",
              "year": 1888,
              "description": "캔버스에 유채"
            },
            ...
          ]
      }
    }
  ```
* **Error Response:**

  * **Code:** 404 Not Found <br />
    **Content:** `{ error : "Artist doesn't exist" }`

  OR

  * **Code:** 500 Internal Server Error <br />
    **Content:** `{ error : "Internal Server Error" }`



#### 4) image 보기

id가 일치하는 image의 정보를 보여준다.

* **URL**

  /image/id

* **Method:**

  `GET` 
  
*  **URL Params**

   
   **Required:**
 
   PARAMETER | TYPE | DESCRIPTION
   ------------ | ------------- | -------------
   id | integer | 보고자 하는 image의 id


   **Optional:**
 
   None

  


* **Data Params**

  None

* **Success Response:**
  
  GET ``/image/1``  

  * **Code:** 200 <br />
    **Content:** <br />
  ```
    {
      "image": {
          "id": 1,
          "image_url": "http://www.vggallery.com/painting/f_0467.jpg",
          "title": "밤의 카페 테라스",
          "year": 1888,
          "description": "캔버스에 유채"
          "arist": {
            "id": 102,
            "name": "빈센트 반 고흐",
            "birth_year": 1853,
            "death_year": 1890,
            "country": "네더란드",
            "genre": "후기 인상주의",
          },
      }
    }
  ```
* **Error Response:**

  * **Code:** 404 Not Found <br />
    **Content:** `{ error : "Image doesn't exist" }`

  OR

  * **Code:** 500 Internal Server Error <br />
    **Content:** `{ error : "Internal Server Error" }`
