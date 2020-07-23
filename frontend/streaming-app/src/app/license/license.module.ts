import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LicenseMaterialWorkspaceModule } from './material.license.workspace.module';
import { LicenseComponent } from './license.component';



@NgModule({
  declarations: [
    LicenseComponent
  ],
  imports: [
    CommonModule,
    LicenseMaterialWorkspaceModule
  ]
})
export class LicenseModule { }
