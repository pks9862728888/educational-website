import { SharedModule } from './../shared/shared.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StudentMaterialWorkspaceModule } from './material.student.workspace.module';
import { studentWorkspaceRoutingComponents, StudentWorkspaceRoutingModule } from './student-workspace-routing.module';
import { ApiService } from '../services/api.service';
import { UiService } from '../services/ui.service';
import { InAppDataTransferService } from '../services/in-app-data-transfer.service';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule, DateAdapter, MAT_DATE_FORMATS } from '@angular/material/core';
import { AppDateAdapter, APP_DATE_FORMATS } from '../format-datepicker';
import { ImageCropperModule } from 'ngx-image-cropper';


@NgModule({
  declarations: [
    studentWorkspaceRoutingComponents
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    ImageCropperModule,
    StudentWorkspaceRoutingModule,
    StudentMaterialWorkspaceModule,
    SharedModule,
    MatDatepickerModule,
    MatNativeDateModule,
  ],
  providers: [
    ApiService,
    UiService,
    InAppDataTransferService,
    {provide: DateAdapter, useClass: AppDateAdapter},
    {provide: MAT_DATE_FORMATS, useValue: APP_DATE_FORMATS}
  ]
})
export class StudentWorkspaceModule { }
