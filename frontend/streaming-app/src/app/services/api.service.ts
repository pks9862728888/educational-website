import { Injectable } from '@angular/core';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';
import { baseUrl } from './../../urls';
import { authTokenName } from 'src/constants';


interface TeacherProfileEditDetails {
  username: string;
  user_profile: {
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
  baseUrlUser = `${this.baseUrl}user/`;
  teacherProfileUrl = `${this.baseUrlUser}user-profile`;
  uploadProfilePictureUrl = `${this.baseUrlUser}upload-profile-picture`;
  deleteProfilePictureUrl = `${this.baseUrlUser}delete-profile-picture/`;
  removeClassProfilePictureUrl = `${this.baseUrlUser}remove-class-profile-picture`;
  profilePictureCountUrl = `${this.baseUrlUser}user-profile-picture-count`;
  listProfilePictureUrl = `${this.baseUrlUser}list-profile-picture`;
  setProfilePictureUrl = `${this.baseUrlUser}set-profile-picture`;
  userProfileDetailsExistsUrl = `${this.baseUrlUser}check-profile-data-exists`

  constructor( private cookieService: CookieService,
               private httpClient: HttpClient ) { }

  // Methods related to teacher profile
  getTeacherProfile() {
    return this.httpClient.get(this.teacherProfileUrl, {headers: this.getAuthHeaders()});
  }

  patchTeacherProfileDetails(profileDetails: TeacherProfileEditDetails) {
    const formattedData = {
      username: profileDetails.username,
      user_profile: {
        first_name: profileDetails.user_profile.first_name || '',
        last_name: profileDetails.user_profile.last_name || '',
        gender: profileDetails.user_profile.gender || '',
        phone: profileDetails.user_profile.phone || '',
        country: profileDetails.user_profile.country,
        date_of_birth: profileDetails.user_profile.date_of_birth || null,
        primary_language: profileDetails.user_profile.primary_language,
        secondary_language: profileDetails.user_profile.secondary_language || '',
        tertiary_language: profileDetails.user_profile.tertiary_language || ''
      }
    };
    return this.httpClient.patch(this.teacherProfileUrl,
                                 JSON.stringify(formattedData),
                                 {headers: this.getAuthHeaders()});
  }

  uploadProfilePicture(data) {
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

  checkUserProfileDetailsExists() {
    return this.httpClient.get(this.userProfileDetailsExistsUrl, {headers: this.getAuthHeaders()});
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
