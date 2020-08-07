import { SectionWorkspaceComponent } from './section-workspace.component';
import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { SectionPermissionComponent } from './section-permission/section-permission.component';


const routes: Routes = [
  {
    path: '',
    component: SectionWorkspaceComponent,
    children: [
      { path: ':name/permissions', component: SectionPermissionComponent }
    ]
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SectionWorkspaceRoutingModule {}


export const sectionWorkspaceRoutingComponents = [
  SectionWorkspaceComponent,
  SectionPermissionComponent
];
