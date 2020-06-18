import { Injectable } from '@angular/core';
import { baseUrl } from '../urls';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';

interface TeacherProfileEditDetails {
  username: string;
  teacher_profile: {
    first_name: string;
    last_name: string;
    gender: string;
    phone: string;
    country: string;
    date_of_birth: string;
    primary_language: string;
    secondary_language: string;
    tertiary_language: string;
  };
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  // Urls for communicating with backend
  baseUrl = baseUrl;
  teacherProfileUrl = `${baseUrl}teacher/teacher-profile`;

  constructor( private cookieService: CookieService,
               private httpClient: HttpClient ) { }

  getTeacherProfile() {
    return this.httpClient.get(this.teacherProfileUrl, {headers: this.getAuthHeaders()});
  }

  patchTeacherProfileDetails(profileDetails: TeacherProfileEditDetails) {
    const formattedData = {
      username: profileDetails.username,
      teacher_profile: {
        first_name: profileDetails.teacher_profile.first_name || '',
        last_name: profileDetails.teacher_profile.last_name || '',
        gender: profileDetails.teacher_profile.gender || '',
        phone: profileDetails.teacher_profile.phone || '',
        country: profileDetails.teacher_profile.country,
        date_of_birth: profileDetails.teacher_profile.date_of_birth || null,
        primary_language: profileDetails.teacher_profile.primary_language,
        secondary_language: profileDetails.teacher_profile.secondary_language || '',
        tertiary_language: profileDetails.teacher_profile.tertiary_language || ''
      }
    };
    return this.httpClient.patch(this.teacherProfileUrl,
                                 JSON.stringify(formattedData),
                                 {headers: this.getAuthHeaders()});
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
