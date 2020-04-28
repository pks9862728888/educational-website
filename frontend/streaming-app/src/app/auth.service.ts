import { Injectable } from '@angular/core';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';
import { baseUrl } from '../urls';
import { Subject } from 'rxjs';

interface LoginFormFormat {
  email: string;
  password: string;
}

interface SignupFormFormat {
  email: string;
  username: string;
  password: string;
  userIsStudent: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  // Urls for communicating with backend
  baseUrl = baseUrl;
  signupUrl = `${baseUrl}user/signup`;
  loginUrl = `${baseUrl}user/login`;

  // Headers for sending form data
  headers = new HttpHeaders({
    'Content-Type': 'application/json'
  });

  // Kind of user who is logged in
  userType: string;

  // Creating observable to send response to type of login member
  private userTypeSignalSource = new Subject<string>();
  userTypeSignalSource$ = this.userTypeSignalSource.asObservable();

  // Creating observable to send response in case of user login
  private userLoggedInSignalSource = new Subject<boolean>();
  userLoggedInSignalSource$ = this.userLoggedInSignalSource.asObservable();

  constructor( private cookieService: CookieService,
               private httpClient: HttpClient ) {}

  // Method to signup a new user
  signup(formdata: SignupFormFormat) {
    const body = {
      email: formdata.email,
      username: formdata.username,
      password: formdata.password,
      is_teacher: JSON.stringify(formdata.userIsStudent) === JSON.stringify('false') ? true : false,
      is_student: JSON.stringify(formdata.userIsStudent) === JSON.stringify('true') ? true : false
    };
    return this.httpClient.post(this.signupUrl, JSON.stringify(body), {headers: this.headers});
  }

  // This method logs in new user
  login(formdata: LoginFormFormat) {
    return this.httpClient.post(this.loginUrl, JSON.stringify(formdata), {headers: this.headers});
  }

  // This method sends login status signal as true
  sendLoggedinStatusSignal(status: boolean) {
    this.userLoggedInSignalSource.next(status);
  }

  // This method sends type of logged in user
  getUserType() {
    const userType = this.userType;
    this.userTypeSignalSource.next(userType);
  }

  // This method sets type of logged in user and sends broadcast
  setUserType(user: string) {
    this.userType = user;
    this.getUserType();
  }

  // This function gets authentication header from stored cookies.
  // getAuthHeaders() {
  //   const token = this.cookieService.get('auth-token-edu-website');
  //   return new HttpHeaders({
  //     'Content-Type': 'application/json',
  //     Authorization: `Token ${token}`
  //   });
  // }
}
