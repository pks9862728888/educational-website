import { MaterialSharedModule } from './material.shared.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReloadComponent } from './reload/reload.component';
import { ErrorTextComponent } from './error-text/error-text.component';



@NgModule({
  declarations: [ReloadComponent, ErrorTextComponent],
  imports: [
    CommonModule,
    MaterialSharedModule
  ],
  exports: [
    ReloadComponent,
    ErrorTextComponent
  ]
})
export class SharedModule { }
