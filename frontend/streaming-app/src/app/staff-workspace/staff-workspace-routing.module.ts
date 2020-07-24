import { Routes, RouterModule } from '@angular/router';
import { StaffWorkspaceComponent } from './staff-workspace.component';
import { StaffProfileComponent } from './staff-profile/staff-profile.component';
import { NgModule } from '@angular/core';

const routes: Routes = [
  {
    path: '',
    component: StaffWorkspaceComponent,
    children: [
      { path: '', redirectTo: '/staff-workspace/profile', pathMatch: 'full' },
      { path: 'profile', component: StaffProfileComponent },
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StaffWorkspaceRoutingModule {}

export const staffWorkspaceRoutingComponents = [
  StaffWorkspaceComponent,
  StaffProfileComponent
];
