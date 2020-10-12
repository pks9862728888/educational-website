
import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { TestWorkspaceComponent } from './test-workspace.component';
import { TestDashboardComponent } from './test-dashboard/test-dashboard.component';


const routes: Routes = [
  {
    path: ':subjectSlug/:testSlug',
    component: TestWorkspaceComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: TestDashboardComponent }
    ]
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TestWorkspaceRoutingModule {}

export const testWorkspaceRoutingComponents = [
  TestWorkspaceComponent,
  TestDashboardComponent
];
