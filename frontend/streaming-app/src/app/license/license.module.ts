import { LicenseComponent } from './license.component';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LicenseMaterialWorkspaceModule } from './material.license.workspace.module';
import { LicenseRoutingModule } from './license-routing.module';
import { LicenseCheckoutComponent } from './license-checkout/license-checkout.component';
import { LicenseReviewComponent } from './license-review/license-review.component';


@NgModule({
  declarations: [
    LicenseComponent,
    LicenseCheckoutComponent,
    LicenseReviewComponent
  ],
  imports: [
    CommonModule,
    LicenseMaterialWorkspaceModule,
    LicenseRoutingModule
  ],
  exports: [
    LicenseComponent,
    LicenseCheckoutComponent,
    LicenseReviewComponent
  ]
})
export class LicenseModule { }
