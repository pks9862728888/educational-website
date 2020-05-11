import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StudentWorkspaceComponent } from './student-workspace.component';
import { StudentMaterialWorkspaceModule } from './material.student.workspace.module';
import { StudentProfileComponent } from './student-profile/student-profile.component';
import { AppRoutingModule } from '../app-routing.module';



@NgModule({
  declarations: [
    StudentWorkspaceComponent,
    StudentProfileComponent
  ],
  imports: [
    CommonModule,
    AppRoutingModule,
    StudentMaterialWorkspaceModule,
  ]
})
export class StudentWorkspaceModule { }
