import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TeacherWorkspaceComponent } from './teacher-workspace.component';
import { TeacherMaterialWorkspaceModule } from './material.teacher.workspace.module';
import { AppRoutingModule } from '../app-routing.module';
import { TeacherProfileComponent } from './teacher-profile/teacher-profile.component';


@NgModule({
  declarations: [
    TeacherWorkspaceComponent,
    TeacherProfileComponent,
  ],
  imports: [
    CommonModule,
    AppRoutingModule,
    TeacherMaterialWorkspaceModule,
  ]
})
export class TeacherWorkspaceModule { }
