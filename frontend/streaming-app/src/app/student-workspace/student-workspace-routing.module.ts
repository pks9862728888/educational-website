import { StudentInstitutesComponent } from './../shared/student-institutes/student-institutes.component';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { StudentProfileComponent } from './student-profile/student-profile.component';
import { StudentWorkspaceComponent } from './student-workspace.component';
import { StudentCoursesComponent } from '../shared/student-courses/student-courses.component';

const routes: Routes = [
  {
    path: '',
    component: StudentWorkspaceComponent,
    children: [
      { path: '', redirectTo: '/student-workspace/profile', pathMatch: 'full' },
      { path: 'profile', component: StudentProfileComponent },
      { path: 'institutes', component: StudentInstitutesComponent },
      { path: 'courses', component: StudentCoursesComponent }
    ],
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StudentWorkspaceRoutingModule {}

export const studentWorkspaceRoutingComponents = [
  StudentWorkspaceComponent,
  StudentProfileComponent
];
