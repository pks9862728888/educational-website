import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StaffMaterialWorkspaceModule } from './material.staff.workspace.module';
import { StaffWorkspaceRoutingModule, staffWorkspaceRoutingComponents } from './staff-workspace-routing.module';


@NgModule({
  declarations: [staffWorkspaceRoutingComponents],
  imports: [
    CommonModule,
    StaffWorkspaceRoutingModule,
    StaffMaterialWorkspaceModule,
  ]
})
export class StaffWorkspaceModule { }
