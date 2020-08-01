import { MaterialSharedModule } from './material.shared.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UiReloadComponent } from '../shared/ui-reload/ui-reload.component';
import { UiErrorTextComponent } from './ui-error-text/ui-error-text.component';
import { UiLoadingComponent } from './ui-loading/ui-loading.component';



@NgModule({
  declarations: [
    UiReloadComponent,
    UiErrorTextComponent,
    UiLoadingComponent,
  ],
  imports: [
    CommonModule,
    MaterialSharedModule
  ],
  exports: [
    UiReloadComponent,
    UiErrorTextComponent,
    UiLoadingComponent
  ]
})
export class SharedModule { }
