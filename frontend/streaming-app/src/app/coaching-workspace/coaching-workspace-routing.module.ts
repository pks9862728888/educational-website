import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { LicenseComponent } from '../license/license.component';
import { CoachingProfileComponent } from './coaching-profile/coaching-profile.component';
import { CoachingPermissionsComponent } from './coaching-permissions/coaching-permissions.component';
import { CoachingWorkspaceComponent } from './coaching-workspace.component';



const routes: Routes = [
  {
    path: '',
    component: CoachingWorkspaceComponent,
    children: [
      { path: ':name/profile', component: CoachingProfileComponent },
      { path: ':name/permissions', component: CoachingPermissionsComponent },
      { path: ':name/license', component: LicenseComponent }
    ],
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CoachingWorkspaceRoutingModule {}

export const coachingWorkspaceRoutingComponents = [
  CoachingWorkspaceComponent,
  CoachingProfileComponent,
  CoachingPermissionsComponent,
];
