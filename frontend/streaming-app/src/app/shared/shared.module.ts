import { MaterialSharedModule } from './material.shared.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UiReloadComponent } from '../shared/ui-reload/ui-reload.component';
import { UiErrorTextComponent } from './ui-error-text/ui-error-text.component';



@NgModule({
  declarations: [UiReloadComponent, UiErrorTextComponent],
  imports: [
    CommonModule,
    MaterialSharedModule
  ],
  exports: [
    UiReloadComponent,
    UiErrorTextComponent
  ]
})
export class SharedModule { }
