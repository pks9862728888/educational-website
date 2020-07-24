import { NgModule } from "@angular/core";
import { RouterModule, Routes } from '@angular/router';

import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { SignupComponent } from './signup/signup.component';
import { LoginComponent } from './login/login.component';


const routes: Routes = [
  {
    path: '',
    children: [
      { path: 'login', component: LoginComponent },
      { path: 'signUp', component: SignupComponent },
      { path: 'forgot-password', component: ForgotPasswordComponent },
    ]
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AuthRoutingModule {}

export const authRoutingComponents = [
  LoginComponent,
  SignupComponent,
  ForgotPasswordComponent
];
