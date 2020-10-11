import { SharedModule } from './../shared/shared.module';
import { ReactiveFormsModule } from '@angular/forms';
import { LicenseComponent } from './license.component';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LicenseMaterialWorkspaceModule } from './material.license.workspace.module';
import { WindowRefService } from '../services/window-ref.service';
import { licenseRoutingComponents, LicenseRoutingModule } from './license.routing.module';


@NgModule({
  declarations: [
    licenseRoutingComponents
  ],
  imports: [
    CommonModule,
    LicenseMaterialWorkspaceModule,
    ReactiveFormsModule,
    SharedModule,
    LicenseRoutingModule
  ],
  exports: [],
  providers: [WindowRefService]
})
export class LicenseModule { }
