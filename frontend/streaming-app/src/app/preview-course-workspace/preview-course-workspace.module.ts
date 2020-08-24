import { SharedModule } from './../shared/shared.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PreviewCourseRoutingModule, previewCourseRoutingComponents } from './preview-course-routing.module';
import { MaterialPreviewCourseModule } from './material-preview-course';



@NgModule({
  declarations: [
    previewCourseRoutingComponents
  ],
  imports: [
    CommonModule,
    PreviewCourseRoutingModule,
    MaterialPreviewCourseModule,
    SharedModule
  ]
})
export class PreviewCourseWorkspaceModule { }
