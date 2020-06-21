import { Injectable } from '@angular/core';
import { baseUrl } from '../urls';
import { HttpHeaders, HttpClient, HttpRequest } from '@angular/common/http';
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
  uploadProfilePictureUrl = `${baseUrl}user/upload-profile-picture`;

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

  uploadProfilePicture(data) {
    // Preparing data for uploading
    const formData = new FormData();
    formData.append('image', data.profilePictureToUpload, data.profilePictureToUpload.name);
    formData.append('class_profile_picture', data.class_profile_picture);
    formData.append('public_profile_picture', data.public_profile_picture);

    return this.httpClient.post(
      this.uploadProfilePictureUrl, formData, {
        headers: this.getMultipartAuthHeaders(),
        reportProgress: true,
        observe: 'events'
      });
  }

  // Loads token from storage
  loadToken() {
    return this.cookieService.get('auth-token-edu-website');
  }

  // This function gets authentication header from stored cookies.
  getAuthHeaders() {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Token ${this.loadToken()}`
    });
  }

  getMultipartAuthHeaders() {
    return new HttpHeaders({
      Authorization: `Token ${this.loadToken()}`
    });
  }
}
