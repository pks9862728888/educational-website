import { DownloadService } from './../services/download.service';
import { ReactiveFormsModule } from '@angular/forms';
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


@NgModule({
  declarations: [
    subjectWorkspaceRoutingComponents,
    ViewVideoComponent,
    ViewPdfComponent,
    ViewImageComponent,
  ],
  imports: [
    CommonModule,
    SubjectWorkspaceRoutingModule,
    MaterialSubjectWorkspaceModule,
    SharedModule,
    MatInputModule,
    ReactiveFormsModule
  ],
  providers: [
    InstituteApiService,
    InAppDataTransferService,
    DownloadService
  ]
})
export class SubjectWorkspaceModule { }
