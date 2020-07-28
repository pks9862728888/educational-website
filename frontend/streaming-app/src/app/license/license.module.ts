import { SharedModule } from './../shared/shared.module';
import { ReactiveFormsModule } from '@angular/forms';
import { LicenseComponent } from './license.component';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LicenseMaterialWorkspaceModule } from './material.license.workspace.module';
import { LicenseCheckoutComponent } from './license-checkout/license-checkout.component';
import { LicenseReviewComponent } from './license-review/license-review.component';
import { WindowRefService } from '../services/window-ref.service';
import { PurchaseLicenseComponent } from './purchase-license/purchase-license.component';


@NgModule({
  declarations: [
    LicenseComponent,
    LicenseCheckoutComponent,
    LicenseReviewComponent,
    PurchaseLicenseComponent,
  ],
  imports: [
    CommonModule,
    LicenseMaterialWorkspaceModule,
    ReactiveFormsModule,
    SharedModule
  ],
  exports: [
    LicenseComponent,
    LicenseCheckoutComponent,
    LicenseReviewComponent,
    PurchaseLicenseComponent
  ],
  providers: [WindowRefService]
})
export class LicenseModule { }
