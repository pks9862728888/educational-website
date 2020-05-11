import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StaffWorkspaceComponent } from './staff-workspace.component';
import { StaffMaterialWorkspaceModule } from './material.staff.workspace.module';
import { StaffProfileComponent } from './staff-profile/staff-profile.component';
import { AppRoutingModule } from '../app-routing.module';



@NgModule({
  declarations: [
    StaffWorkspaceComponent,
    StaffProfileComponent,
  ],
  imports: [
    CommonModule,
    AppRoutingModule,
    StaffMaterialWorkspaceModule,
  ]
})
export class StaffWorkspaceModule { }
