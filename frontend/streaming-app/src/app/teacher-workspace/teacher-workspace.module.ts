import { SharedModule } from './../shared/shared.module';
import { SnackbarComponent } from './teacher-institute/teacher-institute.component';
import { UiService } from './../services/ui.service';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { TeacherMaterialWorkspaceModule } from './material.teacher.workspace.module';
import { TeacherWorkspaceRoutingModule, teacherWorkspaceRoutingComponents } from './teacher-workspace-routing.module';
import { CreateInstituteComponent } from './teacher-institute/create-institute/create-institute.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { ApiService } from '../services/api.service';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule, DateAdapter, MAT_DATE_FORMATS } from '@angular/material/core';
import { AppDateAdapter, APP_DATE_FORMATS } from '../format-datepicker';
import { UploadProfilePictureComponent } from './teacher-profile/upload-profile-picture/upload-profile-picture.component';
import { ImageCropperModule } from 'ngx-image-cropper';
import { ChooseFromExistingComponent } from './teacher-profile/choose-from-existing/choose-from-existing.component';
import { InAppDataTransferService } from '../services/in-app-data-transfer.service';


@NgModule({
  declarations: [
    UploadProfilePictureComponent,
    ChooseFromExistingComponent,
    CreateInstituteComponent,
    teacherWorkspaceRoutingComponents
  ],
  imports: [
    CommonModule,
    ImageCropperModule,
    FormsModule,
    ReactiveFormsModule,
    FlexLayoutModule,
    TeacherMaterialWorkspaceModule,
    TeacherWorkspaceRoutingModule,
    MatDatepickerModule,
    MatNativeDateModule,
    SharedModule
  ],
  providers: [
    ApiService,
    UiService,
    InAppDataTransferService,
    {provide: DateAdapter, useClass: AppDateAdapter},
    {provide: MAT_DATE_FORMATS, useValue: APP_DATE_FORMATS}
  ],
  entryComponents: [SnackbarComponent]
})
export class TeacherWorkspaceModule { }
