import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TeacherWorkspaceComponent } from './teacher-workspace.component';
import { TeacherMaterialWorkspaceModule } from './material.teacher.workspace.module';
import { AppRoutingModule } from '../app-routing.module';
import { TeacherProfileComponent } from './teacher-profile/teacher-profile.component';
import { TeacherCollegeComponent } from './teacher-college/teacher-college.component';
import { TeacherClassComponent } from './teacher-class/teacher-class.component';
import { TeacherSubjectComponent } from './teacher-subject/teacher-subject.component';
import { TeacherMockTestComponent } from './teacher-mock-test/teacher-mock-test.component';
import { TeacherAssignmentComponent } from './teacher-assignment/teacher-assignment.component';
import { TeacherAttendanceComponent } from './teacher-attendance/teacher-attendance.component';
import { TeacherResourcesComponent } from './teacher-resources/teacher-resources.component';
import { TeacherTimeTableComponent } from './teacher-time-table/teacher-time-table.component';
import { TeacherChatroomComponent } from './teacher-chatroom/teacher-chatroom.component';
import { TeacherFeedbackComponent } from './teacher-feedback/teacher-feedback.component';
import { TeacherAnnouncementComponent } from './teacher-announcement/teacher-announcement.component';
import { TeacherResultComponent } from './teacher-result/teacher-result.component';
import { BlockedMembersComponent } from './blocked-members/blocked-members.component';


@NgModule({
  declarations: [
    TeacherWorkspaceComponent,
    TeacherProfileComponent,
    TeacherCollegeComponent,
    TeacherClassComponent,
    TeacherSubjectComponent,
    TeacherMockTestComponent,
    TeacherAssignmentComponent,
    TeacherAttendanceComponent,
    TeacherResourcesComponent,
    TeacherTimeTableComponent,
    TeacherChatroomComponent,
    TeacherFeedbackComponent,
    TeacherAnnouncementComponent,
    TeacherResultComponent,
    BlockedMembersComponent,
  ],
  imports: [
    CommonModule,
    AppRoutingModule,
    TeacherMaterialWorkspaceModule,
  ]
})
export class TeacherWorkspaceModule { }
