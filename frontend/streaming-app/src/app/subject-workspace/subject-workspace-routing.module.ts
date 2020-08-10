import { CreateCourseComponent } from './create-course/create-course.component';
import { PreviewCourseComponent } from './preview-course/preview-course.component';
import { CourseGuidelinesComponent } from './course-guidelines/course-guidelines.component';
import { SubjectOverviewComponent } from './subject-overview/subject-overview.component';
import { Routes, RouterModule } from '@angular/router';
import { NgModule } from "@angular/core";
import { SubjectWorkspaceComponent } from './subject-workspace.component';
import { SubjectPermissionComponent } from './subject-permission/subject-permission.component';


const routes: Routes = [
  {
    path: '',
    component: SubjectWorkspaceComponent,
    children: [
      { path: ':name/overview', component: SubjectOverviewComponent },
      { path: ':name/permissions', component: SubjectPermissionComponent },
      { path: ':name/course-guidelines', component: CourseGuidelinesComponent },
      { path: ':name/create-course', component: CreateCourseComponent },
      { path: ':name/preview-course', component: PreviewCourseComponent },
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
  CreateCourseComponent,
  PreviewCourseComponent
];
