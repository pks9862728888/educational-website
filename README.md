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
        "id": 86,
        "image": "http://192.168.43.26:8000/media/pictures/uploads/user/profile/2020/6/21/c8776d4bca4a.png",
        "uploaded_on": "2020-06-21T20:48:49.670395Z",
        "public_profile_picture": false,
        "class_profile_picture": false
    },
    {
        "id": 87,
        "image": "http://192.168.43.26:8000/media/pictures/uploads/user/profile/2020/6/21/20fe89beea8b.png",
        "uploaded_on": "2020-06-21T20:49:23.115893Z",
        "public_profile_picture": false,
        "class_profile_picture": false
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

**Error:**
```
{
    "detail": "Authentication credentials were not provided."
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

**Error:**
```
{
    "detail": "Authentication credentials were not provided."
}
```

## User Profile Profile Picture Count url
**URL:** https://127.0.0.1:8000/user/user-profile-picture-count

**Allowed methods** POST

**Response:** 
Returns the total number of profile picture available.
```
{
    "count": 4
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
_______________________________________________________________________________________________________________________________________
## Teacher Profile url
**URL:** https://127.0.0.1:8000/institute/institute-min-details-teacher-admin

**Allowed methods** GET

**Scope** Teacher only

**GET Response JSON format:**
```
[
    {
        "user": 3,
        "name": "temp institute teacher 1",
        "country": "IN",
        "institute_category": "A",
        "created_date": "2020-06-25T11:31:21.445568Z",
        "institute_profile": {
            "motto": "",
            "email": "teacher1@gmail.com",
            "phone": "",
            "website_url": "",
            "recognition": "ICSE",
            "state": ""
        },
        "institute_logo": {
            "image": "http://127.0.0.1:8000/media/pictures/uploads/institute/logo/2020/6/26/ff8c4778-3a85-4405-aee8-a841a3040648.png"
        }
    },
    {
        "user": 3,
        "name": "institute 2 teacher1",
        "country": "IN",
        "institute_category": "M",
        "created_date": "2020-06-26T08:18:19.908881Z",
        "institute_profile": {
            "motto": "",
            "email": "",
            "phone": "",
            "website_url": "",
            "recognition": "",
            "state": ""
        },
        "institute_logo": {}
    }
]
```
