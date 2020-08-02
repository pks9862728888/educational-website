import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialSharedModule } from './material.shared.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UiReloadComponent } from '../shared/ui-reload/ui-reload.component';
import { UiErrorTextComponent } from './ui-error-text/ui-error-text.component';
import { UiLoadingComponent } from './ui-loading/ui-loading.component';
import { ClassComponent } from './class/class.component';
import { UiSuccessTextComponent } from './ui-success-text/ui-success-text.component';



@NgModule({
  declarations: [
    UiReloadComponent,
    UiErrorTextComponent,
    UiSuccessTextComponent,
    UiLoadingComponent,
    ClassComponent,
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
    ClassComponent
  ]
})
export class SharedModule { }
