import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { TeacherWorkspaceComponent } from './teacher-workspace.component';
import { TeacherMaterialWorkspaceModule } from './material.teacher.workspace.module';
import { AppRoutingModule } from '../app-routing.module';
import { TeacherProfileComponent } from './teacher-profile/teacher-profile.component';
import { TeacherCollegeComponent } from './teacher-college/teacher-college.component';
import { TeacherChatroomComponent } from './teacher-chatroom/teacher-chatroom.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { ApiService } from '../api.service';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule, DateAdapter, MAT_DATE_FORMATS } from '@angular/material/core';
import { AppDateAdapter, APP_DATE_FORMATS } from '../format-datepicker';
import { UploadProfilePictureComponent } from './teacher-profile/upload-profile-picture/upload-profile-picture.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ImageCropperModule } from 'ngx-image-cropper';
import { ChooseFromExistingComponent } from './teacher-profile/choose-from-existing/choose-from-existing.component';
import { CreateCollegeComponent } from './teacher-college/create-college/create-college.component';
import { CollegePreviewComponent } from './college/college-preview/college-preview.component';
import { RouterModule } from '@angular/router';
import { PermissionsComponent } from './college/permissions/permissions.component';
import { ClassesComponent } from './college/classes/classes.component';


@NgModule({
  declarations: [
    UploadProfilePictureComponent,
    TeacherWorkspaceComponent,
    TeacherProfileComponent,
    TeacherCollegeComponent,
    TeacherChatroomComponent,
    UploadProfilePictureComponent,
    ChooseFromExistingComponent,
    CreateCollegeComponent,
    CollegePreviewComponent,
    PermissionsComponent,
    ClassesComponent,
  ],
  imports: [
    RouterModule,
    CommonModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    ImageCropperModule,
    FormsModule,
    ReactiveFormsModule,
    FlexLayoutModule,
    TeacherMaterialWorkspaceModule,
    MatDatepickerModule,
    MatNativeDateModule
  ],
  providers: [
    ApiService,
    {provide: DateAdapter, useClass: AppDateAdapter},
    {provide: MAT_DATE_FORMATS, useValue: APP_DATE_FORMATS}
  ]
})
export class TeacherWorkspaceModule { }
