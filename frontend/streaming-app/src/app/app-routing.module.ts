import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { MainComponent } from './main/main.component';
import { SignupComponent } from './auth/signup/signup.component';
import { LoginComponent } from './auth/login/login.component';
import { ForgotPasswordComponent } from './auth/forgot-password/forgot-password.component';
import { WorkspaceComponent } from './workspace/workspace.component';
import { StaffComponent } from './workspace/staff/staff.component';
import { StudentComponent } from './workspace/student/student.component';
import { TeacherComponent } from './workspace/teacher/teacher.component';


const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: MainComponent },
  { path: 'login', component: LoginComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'forgot-password', component: ForgotPasswordComponent},
  { path: 'workspace',
    component: WorkspaceComponent,
    children: [
      { path: 'student-workspace', component: StudentComponent },
      { path: 'teacher-workspace', component: TeacherComponent},
      { path: 'staff-workspace', component: StaffComponent }
    ]},
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

export const routingComponents = [
  MainComponent,
  SignupComponent,
  LoginComponent,
  PageNotFoundComponent,
];
