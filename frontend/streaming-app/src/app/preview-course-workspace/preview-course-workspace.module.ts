import { InAppDataTransferService } from './../services/in-app-data-transfer.service';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { SharedModule } from './../shared/shared.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PreviewCourseRoutingModule, previewCourseRoutingComponents } from './preview-course-routing.module';
import { MaterialPreviewCourseModule } from './material-preview-course';
import { PreviewVideoComponent } from './preview-video/preview-video.component';
import { PreviewPdfComponent } from './preview-pdf/preview-pdf.component';
import { PreviewImageComponent } from './preview-image/preview-image.component';
import { NgxExtendedPdfViewerModule } from 'ngx-extended-pdf-viewer';



@NgModule({
  declarations: [
    previewCourseRoutingComponents,
    PreviewVideoComponent,
    PreviewPdfComponent,
    PreviewImageComponent
  ],
  imports: [
    CommonModule,
    PreviewCourseRoutingModule,
    MaterialPreviewCourseModule,
    SharedModule,
    NgxExtendedPdfViewerModule
  ],
  providers: [
    InstituteApiService,
    InAppDataTransferService
  ]
})
export class PreviewCourseWorkspaceModule { }
