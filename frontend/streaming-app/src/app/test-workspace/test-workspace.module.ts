import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { testWorkspaceRoutingComponents, TestWorkspaceRoutingModule } from './test-workspace-routing.module';
import { InstituteApiService } from '../services/institute-api.service';
import { UiService } from '../services/ui.service';
import { InAppDataTransferService } from '../services/in-app-data-transfer.service';
import { MaterialTestWorkspaceModule } from './material-test-workspace';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '../shared/shared.module';
import { MatInputModule } from '@angular/material/input';
import { NgxExtendedPdfViewerModule } from 'ngx-extended-pdf-viewer';
import { TestDashboardDetailsComponent } from './test-dashboard-details/test-dashboard-details.component';
import { TestSetControlsComponent } from './test-set-controls/test-set-controls.component';
import { TestAssignQuestionPaperComponent } from './test-assign-question-paper/test-assign-question-paper.component';
import { TestMonitorProgressComponent } from './test-monitor-progress/test-monitor-progress.component';
import { TestAnswerCheckingComponent } from './test-answer-checking/test-answer-checking.component';
import { TestPublishResultComponent } from './test-publish-result/test-publish-result.component';
import { TestPerformanceAnalysisComponent } from './test-performance-analysis/test-performance-analysis.component';


@NgModule({
  declarations: [
    testWorkspaceRoutingComponents,
    TestDashboardDetailsComponent,
    TestSetControlsComponent,
    TestAssignQuestionPaperComponent,
    TestMonitorProgressComponent,
    TestAnswerCheckingComponent,
    TestPublishResultComponent,
    TestPerformanceAnalysisComponent,
  ],
  imports: [
    CommonModule,
    FormsModule,
    TestWorkspaceRoutingModule,
    MaterialTestWorkspaceModule,
    SharedModule,
    MatInputModule,
    ReactiveFormsModule,
    NgxExtendedPdfViewerModule
  ],
  providers: [
    InstituteApiService,
    InAppDataTransferService,
    UiService
  ]
})
export class TestWorkspaceModule { }
