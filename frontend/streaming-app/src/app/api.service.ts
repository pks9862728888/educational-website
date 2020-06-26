import { Injectable } from '@angular/core';
import { baseUrl } from '../urls';
import { HttpHeaders, HttpClient, HttpRequest } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';
import { authTokenName } from 'src/constants';

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

interface SetProfilePictureData {
  id: string;
  class_profile_picture: boolean;
  public_profile_picture: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  // Urls for communicating with backend
  baseUrl = baseUrl;
  teacherProfileUrl = `${baseUrl}teacher/teacher-profile`;
  uploadProfilePictureUrl = `${baseUrl}user/upload-profile-picture`;
  deleteProfilePictureUrl = `${baseUrl}user/delete-profile-picture/`;
  removeClassProfilePictureUrl = `${baseUrl}user/remove-class-profile-picture`;
  profilePictureCountUrl = `${baseUrl}user/user-profile-picture-count`;
  listProfilePictureUrl = `${baseUrl}user/list-profile-picture`;
  setProfilePictureUrl = `${baseUrl}user/set-profile-picture`;

  constructor( private cookieService: CookieService,
               private httpClient: HttpClient ) { }

  // Methods related to teacher profile
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
        headers: this.getTokenAuthHeaders(),
        reportProgress: true,
        observe: 'events'
      });
  }

  deleteCurrentProfilePicture(id: string) {
    const completeUrl = this.deleteProfilePictureUrl + id;

    return this.httpClient.delete(completeUrl, {headers: this.getTokenAuthHeaders()});
  }

  removeCurrentClassProfilePicture() {
    return this.httpClient.post(this.removeClassProfilePictureUrl, {}, {headers: this.getTokenAuthHeaders()});
  }

  getProfilePictureCount() {
    return this.httpClient.get(this.profilePictureCountUrl, {headers: this.getTokenAuthHeaders()});
  }

  listProfilePicture() {
    return this.httpClient.get(this.listProfilePictureUrl, {headers: this.getTokenAuthHeaders()});
  }

  setUserProfilePicture(data: SetProfilePictureData) {
    return this.httpClient.post(this.setProfilePictureUrl, JSON.stringify(data), {headers: this.getAuthHeaders()});
  }

  // To load token from storage
  loadToken() {
    return this.cookieService.get(authTokenName);
  }

  // This function gets authentication header from stored cookies.
  getAuthHeaders() {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Token ${this.loadToken()}`
    });
  }

  getTokenAuthHeaders() {
    return new HttpHeaders({
      Authorization: `Token ${this.loadToken()}`
    });
  }
}
