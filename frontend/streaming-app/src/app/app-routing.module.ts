import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { SignupComponent } from './auth/signup/signup.component';
import { LoginComponent } from './auth/login/login.component';
import { ForgotPasswordComponent } from './auth/forgot-password/forgot-password.component';
import { AboutComponent } from './about/about.component';
import { PricingComponent } from './pricing/pricing.component';
import { TeacherWorkspaceComponent } from './teacher-workspace/teacher-workspace.component';
import { StudentWorkspaceComponent } from './student-workspace/student-workspace.component';
import { StaffWorkspaceComponent } from './staff-workspace/staff-workspace.component';
import { StaffProfileComponent } from './staff-workspace/staff-profile/staff-profile.component';
import { StudentProfileComponent } from './student-workspace/student-profile/student-profile.component';
import { TeacherProfileComponent } from './teacher-workspace/teacher-profile/teacher-profile.component';
import { HelpComponent } from './help/help.component';
import { FeaturesComponent } from './features/features.component';
import { HomeComponent } from './home/home.component';
import { TeacherInstituteComponent } from './teacher-workspace/teacher-institute/teacher-institute.component';
import { TeacherChatroomComponent } from './teacher-workspace/teacher-chatroom/teacher-chatroom.component';
import { SchoolWorkspaceComponent } from './school-workspace/school-workspace.component';
import { SchoolClassesComponent } from './school-workspace/school-classes/school-classes.component';
import { SchoolPermissionsComponent } from './school-workspace/school-permissions/school-permissions.component';
import { SchoolProfileComponent } from './school-workspace/school-profile/school-profile.component';


const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'signUp', component: SignupComponent },
  { path: 'forgot-password', component: ForgotPasswordComponent},
  { path: 'teacher-workspace',
    component: TeacherWorkspaceComponent,
    children: [
      { path: '', redirectTo: '/teacher-workspace/profile', pathMatch: 'full'},
      { path: 'profile', component: TeacherProfileComponent },
      { path: 'institutes', component: TeacherInstituteComponent },
      { path: 'chatrooms', component: TeacherChatroomComponent },
    ]
  },
  {
    path: 'student-workspace',
    component: StudentWorkspaceComponent,
    children: [
      { path: '', redirectTo: '/student-workspace/profile', pathMatch: 'full' },
      { path: 'profile', component: StudentProfileComponent },
    ]
  },
  {
    path: 'staff-workspace',
    component: StaffWorkspaceComponent,
    children: [
      { path: '', redirectTo: '/staff-workspace/profile', pathMatch: 'full' },
      { path: 'profile', component: StaffProfileComponent },
    ]
  },
  {
    path: 'school-workspace',
    component: SchoolWorkspaceComponent,
    children: [
      { path: ':name/profile', component: SchoolProfileComponent },
      { path: ':name/permissions', component: SchoolPermissionsComponent },
      { path: ':name/classes', component: SchoolClassesComponent }
    ]
  },
  { path: 'features', component: FeaturesComponent },
  { path: 'pricing', component: PricingComponent },
  { path: 'about', component: AboutComponent },
  { path: 'help', component: HelpComponent },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

export const routingComponents = [
  SignupComponent,
  LoginComponent,
  ForgotPasswordComponent,
  PageNotFoundComponent,
];
