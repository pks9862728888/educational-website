import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LicenseMaterialWorkspaceModule } from './material.license.workspace.module';
import { licenseRouteComponents, LicenseRoutingModule } from './license-routing.module';


@NgModule({
  declarations: [licenseRouteComponents],
  imports: [
    CommonModule,
    LicenseMaterialWorkspaceModule,
    LicenseRoutingModule
  ],
  exports: [
    licenseRouteComponents
  ]
})
export class LicenseModule { }
