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
import { UiShowAddContentButtonComponent } from './ui-show-add-content-button/ui-show-add-content-button.component';
import { UiAddContentComponent } from './ui-add-content/ui-add-content.component';


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
    UiShowAddContentButtonComponent,
    UiAddContentComponent,
  ],
  imports: [
    CommonModule,
    MaterialSharedModule,
    FormsModule,
    ReactiveFormsModule,
    MatDatepickerModule,
    MatNativeDateModule
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
    UiShowAddContentButtonComponent,
    UiAddContentComponent
  ],
  providers: [
    InstituteApiService,
    UiService,
    {provide: DateAdapter, useClass: AppDateAdapter},
    {provide: MAT_DATE_FORMATS, useValue: APP_DATE_FORMATS}
  ]
})
export class SharedModule { }
