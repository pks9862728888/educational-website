import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  baseUrl = 'http://127.0.0.1:8000/';

  constructor(private cookieService: CookieService ) { }

  // This function gets authentication header from stored cookies.
  getAuthHeaders() {
    const token = this.cookieService.get('auth-token');
    return new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Token ${token}`
    });
  }
}
