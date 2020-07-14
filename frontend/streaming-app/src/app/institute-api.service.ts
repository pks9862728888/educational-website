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


@Injectable({
  providedIn: 'root'
})
export class InstituteApiService {

  // Urls for communicating with backend
  baseUrl = baseUrl;
  instituteMinDetailsAdminUrl = `${baseUrl}institute/institute-min-details-teacher-admin`;
  instituteCreateUrl = `${baseUrl}institute/create`;
  instituteDetailUrl = `${baseUrl}institute/detail/`;
  instituteUserListUrl = `${baseUrl}institute/`
  instituteInvitationMinDetailUrl = `${baseUrl}institute/get-invitation-min-details/`

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
    return this.httpClient.get(this.instituteDetailUrl + instituteSlug, {headers: this.getAuthHeader()});
  }

  // Get list of admins
  getUserList(instituteSlug: string, role:string) {
    return this.httpClient.get(
      this.instituteUserListUrl + instituteSlug + '/' + role + '/get-user-list',
    { headers: this.getAuthHeader() })
  }

  // Get minimum invitation details
  getMinInvitationDetails(invitation_id: number, institute_id: number) {
    return this.httpClient.get(
      this.instituteInvitationMinDetailUrl + invitation_id + '/' + institute_id,
      { headers: this.getAuthHeader() })
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
