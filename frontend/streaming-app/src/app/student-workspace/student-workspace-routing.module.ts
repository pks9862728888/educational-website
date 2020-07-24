import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { StudentProfileComponent } from './student-profile/student-profile.component';
import { StudentWorkspaceComponent } from './student-workspace.component';

const routes: Routes = [
  {
    path: '',
    component: StudentWorkspaceComponent,
    children: [
      { path: '', redirectTo: '/student-workspace/profile', pathMatch: 'full' },
      { path: 'profile', component: StudentProfileComponent },
    ],
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StudentWorkspaceRoutingModule {}

export const studentWorkspaceRoutingComponents = [
  StudentWorkspaceComponent,
  StudentProfileComponent
];