# live-streaming
Live streaming website with django and angular

## User signup url
**URL:** https://127.0.0.1:8000/user/signup

**Fields:** email, username, password, is_teacher, is_student

**Response on successful user creation:** email, username, is_teacher, is_student, is_staff, is_active

## User login url
**URL:** https://127.0.0.1:8000/user/login

**Fields:** email, password

**Response on successful user login:** token, username, is_teacher, is_student, is_staff, is_active
