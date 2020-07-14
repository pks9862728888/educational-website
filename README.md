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

**Response on successful user login:** token, id, username, email, is_teacher, is_student, is_staff, is_active

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
## Institute create url
**URL:** https://127.0.0.1:8000/institute/create

**Allowed methods** POST

**Scope** Teacher only

**POST JSON format:**
```
{
    "user": 2,
    "name": "temp institute 3",
    "country": "AF",
    "institute_category": "E",
    "institute_profile": {
        "institute": 7,
        "motto": "",
        "email": "",
        "phone": "",
        "website_url": "",
        "state": "",
        "pin": "",
        "address": "",
        "recognition": "",
        "primary_language": "EN",
        "secondary_language": "",
        "tertiary_language": ""
    }
}
```

**JSON Response on successful creation**
```
{
    "created": "true",
    "url": "http://127.0.0.1:8000/institute/temp-institute-4"
}
```

## Institute Profile list with min details url
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

## Institute Profile details url
**URL:** https://127.0.0.1:8000/institute/temp-institute-3

**Allowed methods** GET

**Scope** Teacher only

**GET Response JSON format:**
```
{
    "user": 2,
    "name": "temp institute 3",
    "country": "AF",
    "institute_category": "E",
    "institute_slug": "temp-institute-3",
    "institute_profile": {
        "institute": 7,
        "motto": "",
        "email": "",
        "phone": "",
        "website_url": "",
        "state": "",
        "pin": "",
        "address": "",
        "recognition": "",
        "primary_language": "EN",
        "secondary_language": "",
        "tertiary_language": ""
    },
    "institute_statistics": {
        "no_of_admin": 0,
        "no_of_students": 0,
        "no_of_faculties": 0,
        "no_of_staff": 0
    },
    "institute_logo": {
        "image": "http://127.0.0.1:8000/media/pictures/uploads/institute/logo/2020/6/27/eec547eb-83da-4c3d-9bce-9958d12cb74b.png"
    },
    "institute_banner": {
        "image": "http://127.0.0.1:8000/media/pictures/uploads/institute/banner/2020/6/27/f1d042dc-8787-4056-90aa-a33a1a12e6b1.png"
    }
}
```

## Institute Permission add url
**URL:** https://127.0.0.1:8000/institute/temp-institute-3/provide-permission

**Allowed methods** POST

**Scope** Teacher only

**Allowed permissions** ADMIN or "A", STAFF or "S", FACULTY or "F". ***Admin** can invite everyone. **Staff** can invite staff and faculty.*


**POST Request** 
```
{
    "role": "S",
    "invitee": "xyz@gmail.com"
}
```

**Response**
```
{ "status": "INVITED" }
```

**Error**
```
{ "error": "Permission denied." }
```


## Institute Permission accept delete url
**URL:** https://127.0.0.1:8000/institute/temp-institute-3/accept-delete-permission

**Allowed methods** POST

**Scope** Teacher only

**POST request**

For accepting invitation by invitee:
```
{ "operation": "ACCEPT" }
```


For deleting invitation by invitee:
```
{ "operation": "DELETE" }
```


For accepting invitation by inviter:
```
{
    "operation": "DELETE",
    "invitee": "abc@gmail.com"
}
```
Admin can delete any inactive admin, staff, faculty invite request using this url.

Admin can not delete active admin permission.

Staff and faculty can not delete any invites.


**Response**
```
{ "status": "ACCEPTED" or "DELETED }
```

**Error**
```
{ "error": "Permission denied." }
```


## Institute User list with permissions min details url
**URL:** https://127.0.0.1:8000/institute/temp-institute-name/admin/get-user-list

**Allowed methods** GET

**Scope** Teacher only

**Roles** admin, staff, faculty

**GET Response JSON format:**
```
{
    "active_admin_list": [
        {
            "invitation_id": 2,
            "user_id": 1,
            "email": "teacher@gmail.com",
            "image": ""
        }
    ],
    "pending_admin_invites" : []
}
```
