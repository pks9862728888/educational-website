
import { CourseGuidelinesComponent } from './course-guidelines/course-guidelines.component';
import { SubjectOverviewComponent } from './subject-overview/subject-overview.component';
import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { SubjectWorkspaceComponent } from './subject-workspace.component';
import { SubjectPermissionComponent } from './subject-permission/subject-permission.component';
import { SubjectStudentsComponent } from '../shared/subject-students/subject-students.component';
import { CreateCourseComponent } from './create-course/create-course.component';


const routes: Routes = [
  {
    path: '',
    component: SubjectWorkspaceComponent,
    children: [
      { path: ':name/overview', component: SubjectOverviewComponent },
      { path: ':name/permissions', component: SubjectPermissionComponent },
      { path: ':name/students', component: SubjectStudentsComponent },
      { path: ':name/course-guidelines', component: CourseGuidelinesComponent },
      { path: ':name/create-course', component: CreateCourseComponent }
    ]
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SubjectWorkspaceRoutingModule {}

export const subjectWorkspaceRoutingComponents = [
  SubjectWorkspaceComponent,
  SubjectPermissionComponent,
  SubjectOverviewComponent,
  CourseGuidelinesComponent,
  CreateCourseComponent
];
