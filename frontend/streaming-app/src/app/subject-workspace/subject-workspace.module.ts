import { DownloadService } from './../services/download.service';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { InstituteApiService } from './../services/institute-api.service';
import { InAppDataTransferService } from './../services/in-app-data-transfer.service';
import { SharedModule } from './../shared/shared.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { subjectWorkspaceRoutingComponents, SubjectWorkspaceRoutingModule } from './subject-workspace-routing.module';
import { MaterialSubjectWorkspaceModule } from './material-subject-workspace';
import { ViewVideoComponent } from './view-video/view-video.component';
import { ViewPdfComponent } from './view-pdf/view-pdf.component';
import { ViewImageComponent } from './view-image/view-image.component';

import { PdfViewerModule } from 'ng2-pdf-viewer';


@NgModule({
  declarations: [
    subjectWorkspaceRoutingComponents,
    ViewVideoComponent,
    ViewPdfComponent,
    ViewImageComponent,
  ],
  imports: [
    CommonModule,
    FormsModule,
    SubjectWorkspaceRoutingModule,
    MaterialSubjectWorkspaceModule,
    SharedModule,
    MatInputModule,
    ReactiveFormsModule,
    PdfViewerModule
  ],
  providers: [
    InstituteApiService,
    InAppDataTransferService,
    DownloadService
  ]
})
export class SubjectWorkspaceModule { }
