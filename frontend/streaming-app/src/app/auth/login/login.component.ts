import { authTokenName } from './../../../constants';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';

// Format of response from backend server
interface ServerResponse {
  token: string;
  id: string;
  email: string;
  username: string;
  is_active: string;
  is_staff: string;
  is_student: string;
  is_teacher: string;
}

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  loginForm: FormGroup;
  hidePassword = true;
  errorText: string;
  signUpHint = false;
  userType: string;

  constructor( private formBuilder: FormBuilder,
               private authService: AuthService,
               private cookieService: CookieService,
               private router: Router ) {}

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      email: [null, [Validators.required, Validators.email]],
      password: [null, [Validators.required]]
    });
  }

  // To login into account by communicating with backend server
  login() {
    this.authService.login(this.loginForm.value).subscribe(
      (result: ServerResponse) => {
        let expiryDate = new Date();
        expiryDate.setDate(expiryDate.getDate() + 30);
        this.cookieService.set(authTokenName,
          result.token, expiryDate, '/', '192.168.43.25', false, 'Strict');
        sessionStorage.setItem('user_id', result.id);
        if (result.is_teacher) {
          this.userType = 'TEACHER';
          sessionStorage.setItem('is_teacher', result.is_teacher);
        } else if (result.is_student) {
          this.userType = 'STUDENT';
          sessionStorage.setItem('is_student', result.is_student);
        } else if (result.is_staff) {
          this.userType = 'STAFF';
          sessionStorage.setItem('is_staff', result.is_staff);
        }
        this.redirectToAppropriateWorkspace();
      },
      error => {
        if (error.error.non_field_errors) {
          this.errorText = error.error.non_field_errors[0];
          this.signUpHint = true;
        }
      }
    );
  }

  // To close the hint message to create a new account.
  closeMessage() {
    this.signUpHint = false;
  }

  // To redirect to appropriate workspace
  redirectToAppropriateWorkspace() {
    this.authService.sendLoggedInStatusSignal(true);
    if (this.userType === 'STUDENT') {
      this.router.navigate(['/student-workspace']);
    } else if (this.userType === 'TEACHER') {
      this.router.navigate(['/teacher-workspace']);
    } else if (this.userType === 'STAFF') {
      this.router.navigate(['/staff-workspace']);
    }
  }
}
