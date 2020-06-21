# Educational Website
Educational streaming website with django and angular

# Status: Still in development phase

## User signup url
**URL:** https://127.0.0.1:8000/user/signup

**Fields:** email, username, password, is_teacher, is_student

**Response on successful user creation:** email, username, is_teacher, is_student, is_staff, is_active

## User login url
**URL:** https://127.0.0.1:8000/user/login

**Fields:** email, password

**Response on successful user login:** token, username, email, is_teacher, is_student, is_staff, is_active

**Response on errors:** non_field_errors: ['Unable to authenticate with given credentials.']

## Get auth token url
**URL:** https://127.0.0.1:8000/user/get-auth-token

**Fields:** email, password

**Response on successful user login:** token

## List User Profile Picture url
**URL:** https://127.0.0.1:8000/user/list-profile-picture

**Allowed methods** GET

**Response:** 
```
[
    {
        "id": 4,
        "image": "http://127.0.0.1:8000/media/pictures/uploads/user/profile/2020/5/17/15b3b3be-9010-4c99-9882-46f828e15906.png",
        "uploaded_on": "2020-05-17T17:53:57.612261Z",
        "active": false
    },
    {
        "id": 3,
        "image": "http://127.0.0.1:8000/media/pictures/uploads/user/profile/2020/5/17/d7289061-c09c-4af3-8e4a-99444b59f4e3.png",
        "uploaded_on": "2020-05-17T17:48:09.871949Z",
        "active": true
    }
]
```

## User Upload Profile Picture url
**URL:** https://127.0.0.1:8000/user/upload-profile-picture

**Allowed methods** POST

**Fields:** image

**Response:** 
```
{
    "id": 9,
    "image": "http://127.0.0.1:8000/media/pictures/uploads/user/profile/2020/5/19/a41b0657-ee35-4fb5-8d22-f4cdacac8423.png",
    "uploaded_on": "2020-05-19T02:04:22.193723Z",
    "public_profile_picture": true,
    "class_profile_picture": true
}
```

**Errors:**  image, non-field-errors

## User Set Profile Picture url
**URL:** https://127.0.0.1:8000/user/set-profile-picture

**Allowed methods** POST

**Fields:** 
```
{
"id" : 9,
"public_profile_picture": "True",
"class_profile_picture": "False"
}
```

**Response:** 
```
{
    "id": 14,
    "image": "http://127.0.0.1:8000/media/pictures/uploads/user/profile/2020/5/18/968ddd3e-59fa-41d7-a50e-b6c11af67af3.png",
    "uploaded_on": "2020-05-18T14:39:40.394962Z"
}
```

**Errors:**
```
{
    "id": [
        "Please send a valid id"
    ]
}
```

## User Delete Profile Picture url
**URL:** https://127.0.0.1:8000/user/delete-profile-picture/1

**Allowed methods** DELETE

**Response:** 
```
{
    "class_profile_picture_deleted": false,
    "public_profile_picture_deleted": false,
    "deleted": true
}
```

## User Remove Class Profile Picture url
**URL:** https://127.0.0.1:8000/user/remove-class-profile-picture

**Allowed methods** POST

**Response:** 
Returns `true` if the profile picture is removed, else it will return `false`.
```
{
    "removed": true
}
```

## User Remove Public Profile Picture url
**URL:** https://127.0.0.1:8000/user/remove-public-profile-picture

**Allowed methods** POST

**Response:** 
Returns `true` if the profile picture is removed, else it will return `false`.
```
{
    "removed": true
}
```

## Teacher Profile url
**URL:** https://127.0.0.1:8000/teacher/teacher-profile

**Allowed methods** GET, PUT, PATCH

**GET Response JSON format:**
```
{
    "id": "",
    "email": "",
    "username": "",
    "created_date": "",
    "teacher_profile": {
        "first_name": "",
        "last_name": "",
        "gender": "",
        "phone": null,
        "country": "",
        "date_of_birth": null,
        "primary_language": "EN",
        "secondary_language": null,
        "tertiary_language": ""
    },
    "profile_pictures": {
        "id": 3,
        "image": "",
        "uploaded_on": ""
    }
}
```
**PUT, PATCH JSON Format:**
```
{
    "id": 1,
    "email": "",
    "username": "",
    "created_date": "",
    "teacher_profile": {
        "first_name": "",
        "last_name": "",
        "gender": "",
        "phone": null,
        "country": "IN",
        "date_of_birth": null,
        "primary_language": "EN",
        "secondary_language": null,
        "tertiary_language": ""
    }
}
```
