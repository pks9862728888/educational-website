import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../auth.service';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';

// Format of response from backend server
interface ServerResponse {
  token: string;
  email: string;
  username: string;
  is_active: boolean;
  is_staff: boolean;
  is_student: boolean;
  is_teacher: boolean;
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
  signupHint = false;

  constructor( private formBuilder: FormBuilder,
               private authService: AuthService,
               private cookieService: CookieService,
               private router: Router ) {

    // If auth token is already saved then skipping login step
    if (this.cookieService.get('auth-token-edu-website')) {
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
        this.cookieService.set('auth-token-edu-website', result.token);
        localStorage.setItem('username', result.username);
        localStorage.setItem('email', result.email);
        localStorage.setItem('is_teacher', JSON.stringify(result.is_teacher));
        localStorage.setItem('is_student', JSON.stringify(result.is_student));
        localStorage.setItem('is_staff', JSON.stringify(result.is_staff));
        localStorage.setItem('is_active', JSON.stringify(result.is_active));

        // Sending logged in status as broadcast
        this.authService.sendLoggedinStatusSignal(true);

        this.redirectToAppropriateWorkspace();
      },
      error => {
        if (error.error.non_field_errors) {
          this.errorText = error.error.non_field_errors[0];
          this.signupHint = true;
        } else {
          console.log(error);
        }
      }
    );
  }

  // To close the hint message to create a new account.
  closeMessage() {
    this.signupHint = false;
  }

  // To redirect to appropriate workspace
  redirectToAppropriateWorkspace() {
    // Rendering appropriate workspace
    if (localStorage.getItem('is_student') === JSON.stringify(true)) {
      this.router.navigate(['/student-workspace']);
    } else if (localStorage.getItem('is_teacher') === JSON.stringify(true)) {
      this.router.navigate(['/teacher-workspace']);
    } else if (localStorage.getItem('is_staff') === JSON.stringify(true)) {
      this.router.navigate(['/staff-workspace']);
    } else {
      // Get the type of user and then again navigate to appropriate workspace
    }
  }
}
