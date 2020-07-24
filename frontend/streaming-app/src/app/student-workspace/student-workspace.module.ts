import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StudentMaterialWorkspaceModule } from './material.student.workspace.module';
import { studentWorkspaceRoutingComponents, StudentWorkspaceRoutingModule } from './student-workspace-routing.module';

@NgModule({
  declarations: [
    studentWorkspaceRoutingComponents
  ],
  imports: [
    CommonModule,
    StudentWorkspaceRoutingModule,
    StudentMaterialWorkspaceModule,
  ]
})
export class StudentWorkspaceModule { }
