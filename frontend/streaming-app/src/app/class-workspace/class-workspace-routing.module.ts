import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { ClassWorkspaceComponent } from './class-workspace.component';
import { ClassProfileComponent } from './class-profile/class-profile.component';
import { ClassSubjectsComponent } from './class-subjects/class-subjects.component';
import { ClassPermissionsComponent } from './class-permissions/class-permissions.component';

const routes: Routes = [
  {
    path: '',
    component: ClassWorkspaceComponent,
    children: [
      { path: ':name/profile', component: ClassProfileComponent },
      { path: ':name/permissions', component: ClassPermissionsComponent },
      { path: ':name/subjects', component: ClassSubjectsComponent },
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
  ClassSubjectsComponent
]
