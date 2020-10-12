
import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { TestWorkspaceComponent } from './test-workspace.component';
import { TestDashboardComponent } from './test-dashboard/test-dashboard.component';
import { CreateFileQuestionComponent } from './create-file-question/create-file-question.component';
import { CreateImageQuestionComponent } from './create-image-question/create-image-question.component';
import { CreateTypedQuestionComponent } from './create-typed-question/create-typed-question.component';


const routes: Routes = [
  {
    path: ':subjectSlug/:testSlug',
    component: TestWorkspaceComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full'},
      { path: 'dashboard', component: TestDashboardComponent },
      { path: 'create-question-paper/file-mode', component: CreateFileQuestionComponent },
      { path: 'create-question-paper/image-mode', component: CreateImageQuestionComponent },
      { path: 'create-question-paper/typed-mode', component: CreateTypedQuestionComponent }
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
  TestDashboardComponent,
  CreateFileQuestionComponent,
  CreateImageQuestionComponent,
  CreateTypedQuestionComponent
];
