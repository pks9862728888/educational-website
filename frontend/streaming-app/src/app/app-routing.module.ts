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
import { TeacherCollegeComponent } from './teacher-workspace/teacher-college/teacher-college.component';
import { TeacherFeedbackComponent } from './teacher-workspace/teacher-feedback/teacher-feedback.component';
import { TeacherClassComponent } from './teacher-workspace/teacher-class/teacher-class.component';
import { TeacherChatroomComponent } from './teacher-workspace/teacher-chatroom/teacher-chatroom.component';
import { TeacherTimeTableComponent } from './teacher-workspace/teacher-time-table/teacher-time-table.component';
import { TeacherResultComponent } from './teacher-workspace/teacher-result/teacher-result.component';
import { TeacherAnnouncementComponent } from './teacher-workspace/teacher-announcement/teacher-announcement.component';
import { TeacherResourcesComponent } from './teacher-workspace/teacher-resources/teacher-resources.component';
import { TeacherAttendanceComponent } from './teacher-workspace/teacher-attendance/teacher-attendance.component';
import { TeacherMockTestComponent } from './teacher-workspace/teacher-mock-test/teacher-mock-test.component';
import { TeacherSubjectComponent } from './teacher-workspace/teacher-subject/teacher-subject.component';
import { TeacherAssignmentComponent } from './teacher-workspace/teacher-assignment/teacher-assignment.component';
import { BlockedMembersComponent } from './teacher-workspace/blocked-members/blocked-members.component';


const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'forgot-password', component: ForgotPasswordComponent},
  { path: 'teacher-workspace',
    component: TeacherWorkspaceComponent,
    children: [
      { path: '', redirectTo: '/teacher-workspace/profile', pathMatch: 'full'},
      { path: 'profile', component: TeacherProfileComponent },
      { path: 'institutes', component: TeacherCollegeComponent },
      { path: 'classes', component: TeacherClassComponent },
      { path: 'subjects', component: TeacherSubjectComponent },
      { path: 'tests', component: TeacherMockTestComponent },
      { path: 'assignments', component: TeacherAssignmentComponent },
      { path: 'attendance', component: TeacherAttendanceComponent },
      { path: 'resources', component: TeacherResourcesComponent },
      { path: 'time-table', component: TeacherTimeTableComponent },
      { path: 'chatrooms', component: TeacherChatroomComponent },
      { path: 'feedbacks', component: TeacherFeedbackComponent },
      { path: 'announcements', component: TeacherAnnouncementComponent },
      { path: 'results', component: TeacherResultComponent },
      { path: 'disciplinary-queue', component: BlockedMembersComponent },
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
