import { Injectable } from '@angular/core';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';
import { baseUrl } from '../urls';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  // Urls for communicating with backend
  baseUrl = baseUrl;
  signupUrl = `${baseUrl}user/signup`;

  // Headers for sending form data
  headers = new HttpHeaders({
    'Content-Type': 'application/json'
  });

  constructor( private cookieService: CookieService,
               private httpClient: HttpClient ) {}

  // Method to signup a new user
  signup(formdata) {
    const body = {
      email: formdata.email,
      username: formdata.username,
      password: formdata.password,
      is_teacher: JSON.stringify(formdata.userIsStudent) === JSON.stringify('false') ? true : false,
      is_student: JSON.stringify(formdata.userIsStudent) === JSON.stringify('true') ? true : false
    };
    return this.httpClient.post(this.signupUrl, JSON.stringify(body), {headers: this.headers});
  }

  // This function gets authentication header from stored cookies.
  getAuthHeaders() {
    const token = this.cookieService.get('auth-edu-token');
    return new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Token ${token}`
    });
  }
}
