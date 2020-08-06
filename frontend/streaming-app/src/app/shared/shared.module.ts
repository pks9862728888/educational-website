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
  ],
  imports: [
    CommonModule,
    MaterialSharedModule,
    FormsModule,
    ReactiveFormsModule
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
    UiMbCreateFormComponent
  ],
  providers: [
    InstituteApiService,
    UiService
  ]
})
export class SharedModule { }
