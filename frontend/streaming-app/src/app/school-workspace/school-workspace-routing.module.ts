import { StudentInstituteCoursesComponent } from './../shared/student-institute-courses/student-institute-courses.component';
import { PermissionsComponent } from './../shared/permissions/permissions.component';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SchoolWorkspaceComponent } from './school-workspace.component';
import { SchoolProfileComponent } from './school-profile/school-profile.component';
import { ClassComponent } from '../shared/class/class.component';
import { InstituteStudentsComponent } from '../shared/institute-students/institute-students.component';

const routes: Routes = [
  {
    path: '',
    component: SchoolWorkspaceComponent,
    children: [
      { path: ':name/profile', component: SchoolProfileComponent },
      { path: ':name/permissions', component: PermissionsComponent},
      { path: ':name/classes', component: ClassComponent},
      {
        path: ':name/license',
        loadChildren: () => import('../license/license.module').then(m => m.LicenseModule)
      },
      { path: ':name/students', component: InstituteStudentsComponent},
      { path: ':name/student-courses', component: StudentInstituteCoursesComponent}
    ],
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  providers: [
  ]
})
export class SchoolWorkspaceRoutingModule {}

export const schoolWorkspaceRoutingComponents = [
  SchoolWorkspaceComponent,
  SchoolProfileComponent
];
