import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { ClassWorkspaceComponent } from './class-workspace.component';
import { ClassProfileComponent } from './class-profile/class-profile.component';

const routes: Routes = [
  {
    path: '',
    component: ClassWorkspaceComponent,
    children: [
      { path: ':name/profile', component: ClassProfileComponent },
    ]
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ClassWorkspaceRoutingModule {}

export const classWorkspaceRoutingComponents = [
  ClassWorkspaceComponent,
  ClassProfileComponent
]
