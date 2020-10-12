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



@NgModule({
  declarations: [
    testWorkspaceRoutingComponents
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
