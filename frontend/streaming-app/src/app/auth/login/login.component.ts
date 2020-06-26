import { authTokenName } from './../../../constants';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../auth.service';
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

  // For showing error
  errorText: string;

  // For showing register hint
  signUpHint = false;

  constructor( private formBuilder: FormBuilder,
               private authService: AuthService,
               private cookieService: CookieService,
               private router: Router ) {

    // If auth token is already saved then skipping login step
    if (this.cookieService.get(authTokenName)) {
      this.redirectToAppropriateWorkspace();
    }
  }

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
        // Saving the data and navigating to workspace
        this.cookieService.set(authTokenName, result.token);
        sessionStorage.setItem('user_id', result.id);
        sessionStorage.setItem('username', result.username);
        sessionStorage.setItem('email', result.email);
        sessionStorage.setItem('is_teacher', result.is_teacher);
        sessionStorage.setItem('is_student', result.is_student);
        sessionStorage.setItem('is_staff', result.is_staff);
        sessionStorage.setItem('is_active', result.is_active);

        // Sending logged in status as broadcast
        this.authService.sendLoggedInStatusSignal(true);

        this.redirectToAppropriateWorkspace();
      },
      error => {
        if (error.error.non_field_errors) {
          this.errorText = error.error.non_field_errors[0];
          this.signUpHint = true;
        } else {
          console.log(error);
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
    // Rendering appropriate workspace
    if (sessionStorage.getItem('is_student') === JSON.stringify(true)) {
      this.router.navigate(['/student-workspace']);
    } else if (sessionStorage.getItem('is_teacher') === JSON.stringify(true)) {
      this.router.navigate(['/teacher-workspace']);
    } else if (sessionStorage.getItem('is_staff') === JSON.stringify(true)) {
      this.router.navigate(['/staff-workspace']);
    } else {
      // Get the type of user and then again navigate to appropriate workspace
    }
  }
}
