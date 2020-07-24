import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TeacherWorkspaceComponent } from './teacher-workspace.component';
import { TeacherProfileComponent } from './teacher-profile/teacher-profile.component';
import { TeacherInstituteComponent } from './teacher-institute/teacher-institute.component';
import { TeacherChatroomComponent } from './teacher-chatroom/teacher-chatroom.component';


const routes: Routes = [
  {
    path: '',
    component: TeacherWorkspaceComponent,
    children: [
      { path: '', redirectTo: '/teacher-workspace/profile', pathMatch: 'full'},
      { path: 'profile', component: TeacherProfileComponent },
      { path: 'institutes', component: TeacherInstituteComponent },
      { path: 'chatrooms', component: TeacherChatroomComponent },
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TeacherWorkspaceRoutingModule {}

export const teacherWorkspaceRoutingComponents = [
  TeacherWorkspaceComponent,
  TeacherProfileComponent,
  TeacherInstituteComponent,
  TeacherChatroomComponent
];
