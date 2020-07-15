import { HttpClient, HttpHeaders } from '@angular/common/http';
import { baseUrl } from './../urls';
import { CookieService } from 'ngx-cookie-service';
import { Injectable } from '@angular/core';
import { authTokenName } from '../constants';

interface FormDataInterface {
  name: string;
  country: string;
  institute_category: string;
  institute_profile: {
    motto: string;
    email: string;
    phone: string;
    website_url: string;
    state: string;
    pin: string;
    address: string;
    recognition: string;
    primary_language: string;
    secondary_language: string;
    tertiary_language: string;
  };
}

interface InviterUserInterface {
  role: string;
  invitee: string;
}


@Injectable({
  providedIn: 'root'
})
export class InstituteApiService {

  // Urls for communicating with backend
  baseUrl = baseUrl;
  instituteBaseUrl = `${baseUrl}institute/`;
  instituteMinDetailsAdminUrl = `${this.instituteBaseUrl}institute-min-details-teacher-admin`;
  instituteCreateUrl = `${this.instituteBaseUrl}create`;

  getInstituteDetailUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}detail/${instituteSlug}`;
  }

  getUserListUrl(instituteSlug: string, role: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/${role}/get-user-list`;
  }

  getUserInviteUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/provide-permission`;
  }


  constructor( private cookieService: CookieService,
               private httpClient: HttpClient ) { }

  // Get minimum details of institute for admin teacher of institute
  getTeacherAdminInstituteMinDetails() {
    return this.httpClient.get(this.instituteMinDetailsAdminUrl, {headers: this.getAuthHeader()});
  }

  // Create an institute
  createInstitute(fromData: FormDataInterface) {
    return this.httpClient.post(this.instituteCreateUrl, JSON.stringify(fromData), {headers: this.getAuthHeader()});
  }

  // Get institute details
  getInstituteDetails(instituteSlug: string) {
    return this.httpClient.get(this.getInstituteDetailUrl(instituteSlug), {headers: this.getAuthHeader()});
  }

  // Get list of admins
  getUserList(instituteSlug: string, role:string) {
    return this.httpClient.get(
      this.getUserListUrl(instituteSlug, role),
      { headers: this.getAuthHeader() })
  }

  // Invite new user
  inviteUser(instituteSlug: string, payload: InviterUserInterface) {
    return this.httpClient.post(
      this.getUserInviteUrl(instituteSlug), payload,
      { headers: this.getAuthHeader() }
    );
  }

  // To load token from storage
  loadToken() {
    return this.cookieService.get(authTokenName);
  }

  getAuthHeader() {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Token ${this.loadToken()}`
    });
  }

  getAuthTokenHeader() {
    return new HttpHeaders({
      Authorization: `Token ${this.loadToken()}`
    });
  }
}
