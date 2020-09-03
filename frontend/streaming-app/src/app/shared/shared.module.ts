import { ChooseProfilePictureFromExistingComponent } from '../shared/choose-profile-picture-from-existing/choose-profile-picture-from-existing.component';
import { InstituteApiService } from './../services/institute-api.service';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialSharedModule } from './material.shared.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UiReloadComponent } from '../shared/ui-reload/ui-reload.component';
import { UiErrorTextComponent } from './ui-error-text/ui-error-text.component';
import { UiLoadingComponent } from './ui-loading/ui-loading.component';
import { ClassComponent } from './class/class.component';
import { UiSuccessTextComponent } from './ui-success-text/ui-success-text.component';
import { PermissionsComponent } from './permissions/permissions.component';
import { UiDialogComponent } from './ui-dialog/ui-dialog.component';
import { UiService } from '../services/ui.service';
import { UiInlineInviteFormComponent } from './ui-inline-invite-form/ui-inline-invite-form.component';
import { UiMbInviteFormComponent } from './ui-mb-invite-form/ui-mb-invite-form.component';
import { UiInlineCreateFormComponent } from './ui-inline-create-form/ui-inline-create-form.component';
import { UiMbCreateFormComponent } from './ui-mb-create-form/ui-mb-create-form.component';
import { UiUploadVideoComponent } from './ui-upload-video/ui-upload-video.component';
import { UiUploadImageComponent } from './ui-upload-image/ui-upload-image.component';
import { UiUploadPdfComponent } from './ui-upload-pdf/ui-upload-pdf.component';
import { UiAddExternalLinkComponent } from './ui-add-external-link/ui-add-external-link.component';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule, DateAdapter, MAT_DATE_FORMATS } from '@angular/material/core';
import { AppDateAdapter, APP_DATE_FORMATS } from '../format-datepicker';
import { UiActionControlsComponent } from './ui-action-controls/ui-action-controls.component';
import { UiEditStudyMaterialComponent } from './ui-edit-study-material/ui-edit-study-material.component';
import { UiAddContentComponent } from './ui-add-content/ui-add-content.component';
import { UploadProfilePictureComponent } from '../shared/upload-profile-picture/upload-profile-picture.component';
import { ImageCropperModule } from 'ngx-image-cropper';
import { InviteStudentsComponent } from './invite-students/invite-students.component';
import { EditStudentDetailsFormComponent } from './edit-student-details-form/edit-student-details-form.component';
import { StudentInstitutesComponent } from './student-institutes/student-institutes.component';
import { SnackbarComponent } from './snackbar/snackbar.component';
import { ConfirmStudentsDetailsComponent } from './student-institutes/confirm-students-details/confirm-students-details.component';


@NgModule({
  declarations: [
    UiReloadComponent,
    UiErrorTextComponent,
    UiSuccessTextComponent,
    UiLoadingComponent,
    ClassComponent,
    PermissionsComponent,
    UiDialogComponent,
    UiInlineInviteFormComponent,
    UiMbInviteFormComponent,
    UiInlineCreateFormComponent,
    UiMbCreateFormComponent,
    UiUploadVideoComponent,
    UiUploadImageComponent,
    UiUploadPdfComponent,
    UiAddExternalLinkComponent,
    UiActionControlsComponent,
    UiEditStudyMaterialComponent,
    UiAddContentComponent,
    ChooseProfilePictureFromExistingComponent,
    UploadProfilePictureComponent,
    InviteStudentsComponent,
    EditStudentDetailsFormComponent,
    StudentInstitutesComponent,
    SnackbarComponent,
    ConfirmStudentsDetailsComponent
  ],
  imports: [
    CommonModule,
    MaterialSharedModule,
    FormsModule,
    ReactiveFormsModule,
    MatDatepickerModule,
    MatNativeDateModule,
    ImageCropperModule
  ],
  exports: [
    UiReloadComponent,
    UiErrorTextComponent,
    UiSuccessTextComponent,
    UiLoadingComponent,
    ClassComponent,
    PermissionsComponent,
    UiInlineInviteFormComponent,
    UiMbInviteFormComponent,
    UiInlineCreateFormComponent,
    UiMbCreateFormComponent,
    UiUploadVideoComponent,
    UiUploadImageComponent,
    UiUploadPdfComponent,
    UiAddExternalLinkComponent,
    UiEditStudyMaterialComponent,
    UiAddContentComponent,
    ChooseProfilePictureFromExistingComponent,
    UploadProfilePictureComponent,
    InviteStudentsComponent,
    EditStudentDetailsFormComponent,
    StudentInstitutesComponent,
    SnackbarComponent,
    ConfirmStudentsDetailsComponent
  ],
  providers: [
    InstituteApiService,
    UiService,
    {provide: DateAdapter, useClass: AppDateAdapter},
    {provide: MAT_DATE_FORMATS, useValue: APP_DATE_FORMATS}
  ]
})
export class SharedModule { }
