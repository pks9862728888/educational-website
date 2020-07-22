import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { SignupComponent } from './auth/signup/signup.component';
import { LoginComponent } from './auth/login/login.component';
import { ForgotPasswordComponent } from './auth/forgot-password/forgot-password.component';
import { HomeComponent } from './home/home.component';
import { AboutComponent } from './about/about.component';
import { PricingComponent } from './pricing/pricing.component';
import { HelpComponent } from './help/help.component';
import { FeaturesComponent } from './features/features.component';
import { LicenseComponent } from './license/license.component';
import { SitemapComponent } from './sitemap/sitemap.component';
import { TeacherWorkspaceComponent } from './teacher-workspace/teacher-workspace.component';
import { StudentWorkspaceComponent } from './student-workspace/student-workspace.component';
import { StaffWorkspaceComponent } from './staff-workspace/staff-workspace.component';
import { StaffProfileComponent } from './staff-workspace/staff-profile/staff-profile.component';
import { StudentProfileComponent } from './student-workspace/student-profile/student-profile.component';
import { TeacherProfileComponent } from './teacher-workspace/teacher-profile/teacher-profile.component';
import { TeacherInstituteComponent } from './teacher-workspace/teacher-institute/teacher-institute.component';
import { TeacherChatroomComponent } from './teacher-workspace/teacher-chatroom/teacher-chatroom.component';
import { SchoolWorkspaceComponent } from './school-workspace/school-workspace.component';
import { SchoolClassesComponent } from './school-workspace/school-classes/school-classes.component';
import { SchoolPermissionsComponent } from './school-workspace/school-permissions/school-permissions.component';
import { SchoolProfileComponent } from './school-workspace/school-profile/school-profile.component';
import { CollegeWorkspaceComponent } from './college-workspace/college-workspace.component';
import { CollegeProfileComponent } from './college-workspace/college-profile/college-profile.component';
import { CollegePermissionsComponent } from './college-workspace/college-permissions/college-permissions.component';
import { CoachingWorkspaceComponent } from './coaching-workspace/coaching-workspace.component';
import { CoachingPermissionsComponent } from './coaching-workspace/coaching-permissions/coaching-permissions.component';
import { CoachingProfileComponent } from './coaching-workspace/coaching-profile/coaching-profile.component';
import { SignUpLoginGuard,StudentWorkspaceGuard, TeacherWorkspaceGuard,
         StaffWorkspaceGuard, SchoolWorkspaceGuard, CollegeWorkspaceGuard,
         CoachingWorkspaceGuard } from './auth/auth.guard';


const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'login', component: LoginComponent, canActivate: [SignUpLoginGuard] },
  { path: 'signUp', component: SignupComponent, canActivate: [SignUpLoginGuard] },
  { path: 'forgot-password', component: ForgotPasswordComponent},
  { path: 'teacher-workspace',
    component: TeacherWorkspaceComponent,
    children: [
      { path: '', redirectTo: '/teacher-workspace/profile', pathMatch: 'full'},
      { path: 'profile', component: TeacherProfileComponent },
      { path: 'institutes', component: TeacherInstituteComponent },
      { path: 'chatrooms', component: TeacherChatroomComponent },
    ],
    canActivate: [TeacherWorkspaceGuard]
  },
  {
    path: 'student-workspace',
    component: StudentWorkspaceComponent,
    children: [
      { path: '', redirectTo: '/student-workspace/profile', pathMatch: 'full' },
      { path: 'profile', component: StudentProfileComponent },
    ],
    canActivate: [StudentWorkspaceGuard]
  },
  {
    path: 'staff-workspace',
    component: StaffWorkspaceComponent,
    children: [
      { path: '', redirectTo: '/staff-workspace/profile', pathMatch: 'full' },
      { path: 'profile', component: StaffProfileComponent },
    ],
    canActivate: [StaffWorkspaceGuard]
  },
  {
    path: 'school-workspace',
    component: SchoolWorkspaceComponent,
    children: [
      { path: ':name/profile', component: SchoolProfileComponent },
      { path: ':name/permissions', component: SchoolPermissionsComponent },
      { path: ':name/classes', component: SchoolClassesComponent },
      { path: ':name/license', component: LicenseComponent }
    ],
    canActivate: [SchoolWorkspaceGuard]
  },
  {
    path: 'college-workspace',
    component: CollegeWorkspaceComponent,
    children: [
      { path: ':name/profile', component: CollegeProfileComponent },
      { path: ':name/permissions', component: CollegePermissionsComponent },
      { path: ':name/license', component: LicenseComponent },
    ],
    canActivate: [CollegeWorkspaceGuard]
  },
  {
    path: 'coaching-workspace',
    component: CoachingWorkspaceComponent,
    children: [
      { path: ':name/profile', component: CoachingProfileComponent },
      { path: ':name/permissions', component: CoachingPermissionsComponent },
      { path: ':name/license', component: LicenseComponent },
    ],
    canActivate: [CoachingWorkspaceGuard]
  },
  { path: 'features', component: FeaturesComponent },
  { path: 'pricing', component: PricingComponent },
  { path: 'about', component: AboutComponent },
  { path: 'help', component: HelpComponent },
  { path: 'sitemap', component: SitemapComponent },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [
    SignUpLoginGuard,
    TeacherWorkspaceGuard,
    StudentWorkspaceGuard,
    StaffWorkspaceGuard,
    SchoolWorkspaceGuard,
    CollegeWorkspaceGuard,
    CoachingWorkspaceGuard
  ]
})
export class AppRoutingModule { }

export const routingComponents = [
  SignupComponent,
  LoginComponent,
  ForgotPasswordComponent,
  PageNotFoundComponent,
  LicenseComponent,
  SitemapComponent,
];
