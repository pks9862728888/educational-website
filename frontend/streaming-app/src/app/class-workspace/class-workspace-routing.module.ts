import { ClassSectionComponent } from './class-section/class-section.component';
import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { ClassWorkspaceComponent } from './class-workspace.component';
import { ClassProfileComponent } from './class-profile/class-profile.component';
import { ClassSubjectsComponent } from './class-subjects/class-subjects.component';
import { ClassPermissionsComponent } from './class-permissions/class-permissions.component';
import { ClassStudentsComponent } from '../shared/class-students/class-students.component';

const routes: Routes = [
  {
    path: '',
    component: ClassWorkspaceComponent,
    children: [
      { path: ':name/profile', component: ClassProfileComponent },
      { path: ':name/permissions', component: ClassPermissionsComponent },
      { path: ':name/students', component: ClassStudentsComponent },
      { path: ':name/subjects', component: ClassSubjectsComponent },
      { path: ':name/sections', component: ClassSectionComponent }
    ]
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ClassWorkspaceRoutingModule {}

export const classWorkspaceRoutingComponents = [
  ClassWorkspaceComponent,
  ClassProfileComponent,
  ClassPermissionsComponent,
  ClassSubjectsComponent,
  ClassSectionComponent
]
