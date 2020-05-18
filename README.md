# Educational Website
Live streaming website with django and angular

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

## Teacher Profile url
**URL:** https://127.0.0.1:8000/teacher/teacher-profile

**Allowed methods** GET, PUT, PATCH

**GET Response:
`
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
`
**PUT, PATCH Format:
`
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
`
