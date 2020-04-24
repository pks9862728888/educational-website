import { Component, OnInit } from '@angular/core';
import { Validators, FormGroup, FormControl, FormGroupDirective, NgForm, FormBuilder } from '@angular/forms';
import { passwordMatchValidator } from 'src/app/confirm.password.validator';
import { AuthService } from 'src/app/auth.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  constructor( private formBuilder: FormBuilder,
               private authService: AuthService ) { }

  signupForm: FormGroup;

  ngOnInit(): void {
    this.signupForm = this.formBuilder.group({
      email: [null, [Validators.email, Validators.required]],
      username: [null, [Validators.required, Validators.minLength(4)]],
      password: [null, [Validators.required, Validators.minLength(8)]],
      confirmPassword: [null, Validators.required],
      userIsStudent: [null, Validators.required]
    }, { validators: passwordMatchValidator });
  }

  signUp() {
    this.authService.signup(this.signupForm.value).subscribe(
      result => console.log(result),
      error => console.error(error)
    );
  }

}
