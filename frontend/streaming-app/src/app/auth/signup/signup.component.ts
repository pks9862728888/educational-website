import { Component, OnInit } from '@angular/core';
import { Validators, FormGroup, FormBuilder } from '@angular/forms';
import { passwordMatchValidator, usernamePasswordValidator } from 'src/app/custom.validator';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  hidePassword = true;
  hideConfirmPassword = true;
  signupForm: FormGroup;
  serverResponseErrors = {
    emailError: null,
    usernameError: null,
    passwordError: null
  };
  loginHint = false;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router ) {}

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
        this.router.navigate(['/auth/login']);
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
        // this.loginHint = true;
      }
    );
  }

  // Closes login message banner
  closeMessage() {
    this.loginHint = false;
  }
}
