
import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { TestWorkspaceComponent } from './test-workspace.component';
import { TestDashboardComponent } from './test-dashboard/test-dashboard.component';
import { CreateFileQuestionComponent } from './create-file-question/create-file-question.component';
import { CreateImageQuestionComponent } from './create-image-question/create-image-question.component';
import { CreateTypedAllTypeQuestionComponent } from './create-typed-all-type-question/create-typed-all-type-question.component';
import { CreateTypedAutocheckTypeQuestionComponent } from './create-typed-autocheck-type-question/create-typed-autocheck-type-question.component';


const routes: Routes = [
  {
    path: ':subjectSlug/:testSlug',
    component: TestWorkspaceComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full'},
      { path: 'dashboard', component: TestDashboardComponent },
      { path: 'create-question-paper/file-mode', component: CreateFileQuestionComponent },
      { path: 'create-question-paper/image-mode', component: CreateImageQuestionComponent },
      { path: 'create-question-paper/all-question-typed-mode', component: CreateTypedAllTypeQuestionComponent },
      { path: 'create-question-paper/autocheck-question-typed-mode', component: CreateTypedAutocheckTypeQuestionComponent }
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
  CreateTypedAllTypeQuestionComponent,
  CreateTypedAutocheckTypeQuestionComponent
];
