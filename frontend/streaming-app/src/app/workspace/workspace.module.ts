import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StudentComponent } from './student/student.component';
import { TeacherComponent } from './teacher/teacher.component';
import { StaffComponent } from './staff/staff.component';
import { WorkspaceComponent } from './workspace.component';
import { AppRoutingModule } from '../app-routing.module';


@NgModule({
  declarations: [StudentComponent, TeacherComponent, StaffComponent, WorkspaceComponent],
  imports: [
    CommonModule,
    AppRoutingModule
  ]
})
export class WorkspaceModule { }
