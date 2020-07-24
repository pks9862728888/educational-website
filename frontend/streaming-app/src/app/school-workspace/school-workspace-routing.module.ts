import { RouterModule, Routes } from '@angular/router';
import { SchoolWorkspaceComponent } from './school-workspace.component';
import { SchoolProfileComponent } from './school-profile/school-profile.component';
import { SchoolPermissionsComponent } from './school-permissions/school-permissions.component';
import { SchoolClassesComponent } from './school-classes/school-classes.component';
import { NgModule } from '@angular/core';
import { LicenseComponent } from '../license/license.component';


const routes: Routes = [
  {
    path: '',
    component: SchoolWorkspaceComponent,
    children: [
      { path: ':name/profile', component: SchoolProfileComponent },
      { path: ':name/permissions', component: SchoolPermissionsComponent },
      { path: ':name/classes', component: SchoolClassesComponent },
      { path: ':name/license', component: LicenseComponent }
    ],
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SchoolWorkspaceRoutingModule {}

export const schoolWorkspaceRoutingComponents = [
  SchoolWorkspaceComponent,
  SchoolProfileComponent,
  SchoolPermissionsComponent,
  SchoolClassesComponent
];
