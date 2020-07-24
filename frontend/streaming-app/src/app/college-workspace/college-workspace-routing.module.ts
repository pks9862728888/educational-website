import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { LicenseComponent } from '../license/license.component';
import { CollegeProfileComponent } from './college-profile/college-profile.component';
import { CollegePermissionsComponent } from './college-permissions/college-permissions.component';
import { CollegeWorkspaceComponent } from './college-workspace.component';



const routes: Routes = [
  {
    path: '',
    component: CollegeWorkspaceComponent,
    children: [
      { path: ':name/profile', component: CollegeProfileComponent },
      { path: ':name/permissions', component: CollegePermissionsComponent },
      { path: ':name/license', component: LicenseComponent }
    ],
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CollegeWorkspaceRoutingModule {}

export const collegeWorkspaceRoutingComponents = [
  CollegeWorkspaceComponent,
  CollegeProfileComponent,
  CollegePermissionsComponent,
];
