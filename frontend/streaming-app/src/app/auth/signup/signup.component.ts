import { Component, OnInit } from '@angular/core';
import { Validators, FormGroup, FormControl, FormGroupDirective, NgForm, FormBuilder } from '@angular/forms';
import { passwordMatchValidator, usernamePasswordValidator } from 'src/app/custom.validator';
import { AuthService } from 'src/app/auth.service';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  constructor( private cookieService: CookieService,
               private formBuilder: FormBuilder,
               private authService: AuthService,
               private router: Router ) {
    // If auth token is already saved then skipping signup step
    if (this.cookieService.get('auth-token-edu-website')) {
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

  signupForm: FormGroup;

  serverResponseErrors = {
    emailError: null,
    usernameError: null,
    passwordError: null
  };

  // Shows hint to login if user is present already with the email.
  loginHint = false;

  ngOnInit(): void {
    this.signupForm = this.formBuilder.group({
      email: [null, [Validators.email, Validators.required]],
      username: [null, [Validators.required, Validators.minLength(4)]],
      password: [null, [Validators.required, Validators.minLength(8)]],
      confirmPassword: [null, Validators.required],
      userIsStudent: [null, Validators.required]
    }, { validator: [passwordMatchValidator, usernamePasswordValidator] });
  }

  // Used to sign in. If successful, then navigates to login page else displays errors.
  signUp() {
    this.authService.signup(this.signupForm.value).subscribe(
      result => {
        this.router.navigate(['/login']);
      },
      error => {
        this.serverResponseErrors.emailError = error.error.email ? error.error.email[0] : null;
        this.serverResponseErrors.usernameError = error.error.username ? error.error.username[0] : null;
        this.serverResponseErrors.passwordError = error.error.password ? error.error.password[0] : null;
        this.signupForm.reset({
          email: this.signupForm.controls.email.value,
          username: this.signupForm.controls.username.value,
          userIsStudent: this.signupForm.controls.userIsStudent.value
        });
        this.loginHint = true;
      }
    );
  }

  // Closes login message banner
  closeMessage() {
    this.loginHint = false;
  }
}
