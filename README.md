# Django_rest_example



### Environment

- docker

- docker-compose

- python 3.7

  

### Run Project

```
$git clone https://github.com/LazyerIJ/Django_rest_example
```



1) Run with docker

```
docker-compose up -d
```

2. Run from code

```
$python -m pip install -r requirements.txt
$python manage.py runserver
```





### Project explanation

- 모든 입출력은 REST API를 이용한 JSON 데이터로 이루어집니다.
- 회원가입 / 문자인증 / 로그인 / 로그아웃 / 비밀번호 재설정 / 정보확인 기능으로 이루어져 있습니다.
  - 회원가입
    - POST
    - /api/signup/
  - 비밀번호 재설정
    - UPDATE
    - /api/signup
  - 로그인
    - POST
    - /api/login/
  - 로그아웃
    - POST
    - /api/logout/
  - 문자인증
    - POST
    - /api/auth/
  - 정보확인
    - GET
    - /api/user/



### Example

1) 회원가입 (POST. /api/signup/)
   ```json
   {
       "phone_number": "01012341234",
       "password": "1234",
       "email": "ablyproject@gmail.com",
       "nickname": "lazyer",
       "name": "KimInJu"
   }
   ```

   ```text
   curl --location \
                   --request POST "http://127.0.0.1:8000/api/signup/" \
                   --header "Content-Type: application/json" \
                   --data-raw "{
                   \"phone_number\": \"01012341234\",
                   \"password\": \"1234\",
                   \"email\": \"ablyproject@gmail.com\",
                   \"nickname\": \"lazyer\",
                   \"name\": \"123\"
                   }
   ```

2) 문자인증 (POST. /api/auth/)
   ```json
   {
       "phone_number": "01012341234",
       "auth_number": "0000"
   }
   ```

   ```
   curl --location --request POST "http://127.0.0.1:8000/api/auth/" \
                   --header "Content-Type: application/json" \
                   --data-raw "{
                   \"phone_number\": \"01012341234\",
                   \"auth_number\": \"0000\"
                   }
   ```

3) 로그인 (POST. /api/login/)
   ```
   {
       "phone_number": "01012341234",
       "password": "1234"
   }
   ```

   ```
   curl --location \
                   --request POST "http://127.0.0.1:8000/api/login/" \
                   --header "Content-Type: application/json" \
                   --data-raw "{
                   \"phone_number\": \"01012341234\",
                   \"password\": \"4321\"
                   }"
   ```

4) 정보확인 (GET. /api/user/)
   ```
   curl --location \
               --request GET "http://127.0.0.1:8000/api/user?phone_number=01012341234" \
               --data-raw "
   ```

5) 로그아웃 (POST. /api/logout/)
   ```
   {
       "phone_number": "01012341234",
       "password": "1234"
   }
   ```

   ```
   curl --location \
                   --request POST "http://127.0.0.1:8000/api/logout/" \
                   --header "Content-Type: application/json" \
                   --data-raw "{
                   \"phone_number\": \"01012341234\",
                   \"password\": \"1234\"
                   }"
   ```

   

### Test code

ablyproject/tests/test_api에 테스트 코드가 작성되어 있으며 몇개의 시나리오 테스트가 있습니다.

테스트 코드의 출력은 아래와 같습니다.

```
python manage.py test tests
```



```
[*]
        1. 로그인 -> 회원가입을 하지 않았기 때문에 오류 발생
        2. 정보 확인 -> 로그인을 하지 않았기 때문에 오류 발생

>>do_user_login:  400 존재하지 않는 사용자입니다.
>>do_user_info_get:  400 존재하지 않는 사용자입니다.
.[*]
        1. 회원가입
        2. 문자인증
        3. 로그인
        4. 정보확인

>>do_user_signup:  200 SMS 인증문자 발송에 성공하였습니다.
>>do_user_auth:  200 SMS 인증에 성공하였습니다.
>>do_user_login:  200 로그인에 성공하였습니다.
>>do_user_info_get:  201 요청하신 작업이 정상수행 되었습니다.
.[*]
        1. 회원가입
        2. 문자인증
        3. 로그인
        4. 로그인 -> 이미 로그인 하였으므로 오류발생
        
>>do_user_signup:  200 SMS 인증문자 발송에 성공하였습니다.
>>do_user_auth:  200 SMS 인증에 성공하였습니다.
>>do_user_login:  200 로그인에 성공하였습니다.
>>do_user_login:  400 이미 로그인되어 있습니다.
.[*]
        1. 회원가입
        2. 문자인증
        3. 로그인
        4. 로그아웃
        5. 로그아웃 -> 이미 로그아웃 하였으므로 오류발생

>>do_user_signup:  200 SMS 인증문자 발송에 성공하였습니다.
>>do_user_auth:  200 SMS 인증에 성공하였습니다.
>>do_user_login:  200 로그인에 성공하였습니다.
>>do_user_logout:  200 로그아웃에 성공하였습니다.
>>do_user_logout:  400 이미 로그아웃되어 있습니다.
.[*]
        1. 회원가입
        2. 문자인증
        3. 로그인(잘못된 패스워드) -> 패스워드가 틀렸으므로 오류발생

>>do_user_signup:  200 SMS 인증문자 발송에 성공하였습니다.
>>do_user_auth:  200 SMS 인증에 성공하였습니다.
>>do_user_login_with_wrong_password:  400 패스워드가 잘못 입력되었습니다.
```



### Logging

- 로그는 config/settings/base./py 에서 경로 설정이 가능합니다.

- 기본적으로 logs 폴더 아래에 생성됩니다.

  - ablyproejct_api.log 예시
    ```
    [2022/08/19 22:33:15][INFO][api  :166 ][01012341234][100003]존재하지 않는 사용자입니다.
    [2022/08/19 22:33:15][INFO][api  :252 ][01012341234][100003]존재하지 않는 사용자입니다.
    [2022/08/19 22:33:15][INFO][api  :73  ][01012341234][102002]SMS 인증문자 발송에 성공하였습니다.
    [2022/08/19 22:33:15][INFO][api  :144 ][01012341234][102003]SMS 문자인증에 성공하였습니다.
    [2022/08/19 22:33:15][INFO][api  :190 ][01012341234][101001]로그인에 성공하였습니다.
    [2022/08/19 22:33:15][INFO][api  :265 ][01012341234][100000]요청하신 작업이 정상수행 되었습니다.
    [2022/08/19 22:33:15][INFO][api  :73  ][01012341234][102002]SMS 인증문자 발송에 성공하였습니다.
    [2022/08/19 22:33:15][INFO][api  :144 ][01012341234][102003]SMS 문자인증에 성공하였습니다.
    [2022/08/19 22:33:15][INFO][api  :190 ][01012341234][101001]로그인에 성공하였습니다.
    [2022/08/19 22:33:16][INFO][api  :184 ][01012341234][101003]이미 로그인되어 있습니다.
    [2022/08/19 22:33:16][INFO][api  :73  ][01012341234][102002]SMS 인증문자 발송에 성공하였습니다.
    [2022/08/19 22:33:16][INFO][api  :144 ][01012341234][102003]SMS 문자인증에 성공하였습니다.
    [2022/08/19 22:33:16][INFO][api  :190 ][01012341234][101001]로그인에 성공하였습니다.
    [2022/08/19 22:33:16][INFO][api  :230 ][01012341234][101002]로그아웃에 성공하였습니다.
    [2022/08/19 22:33:16][INFO][api  :224 ][01012341234][101004]이미 로그아웃되어 있습니다.
    [2022/08/19 22:33:17][INFO][api  :73  ][01012341234][102002]SMS 인증문자 발송에 성공하였습니다.
    [2022/08/19 22:33:17][INFO][api  :144 ][01012341234][102003]SMS 문자인증에 성공하였습니다.
    [2022/08/19 22:33:17][INFO][api  :172 ][01012341234][100003]패스워드가 잘못 입력되었습니다.
    ```

  - ablyproject_app.log 예시
    ```
    [2022/08/19 22:37:02][WARNING][django.request:241 ]Bad Request: /api/login/
    [2022/08/19 22:37:02][WARNING][django.request:241 ]Bad Request: /api/user/
    [2022/08/19 22:37:03][WARNING][django.request:241 ]Bad Request: /api/login/
    [2022/08/19 22:37:04][WARNING][django.request:241 ]Bad Request: /api/logout/
    [2022/08/19 22:37:04][WARNING][django.request:241 ]Bad Request: /api/login/
    ```

    

