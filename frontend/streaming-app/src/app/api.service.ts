import { Injectable } from '@angular/core';
import { baseUrl } from '../urls';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  // Urls for communicating with backend
  baseUrl = baseUrl;
  teacherProfileUrl = `${baseUrl}teacher/teacher-profile`;

  // Headers for sending form data
  headers = new HttpHeaders({
    'Content-Type': 'application/json'
  });


  constructor( private cookieService: CookieService,
               private httpClient: HttpClient ) { }

  getTeacherProfile() {
    return this.httpClient.get(this.teacherProfileUrl, {headers: this.getAuthHeaders()});
  }

  // This function gets authentication header from stored cookies.
  getAuthHeaders() {
    const token = this.cookieService.get('auth-token-edu-website');
    return new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Token ${token}`
    });
  }
}
