import { ReactiveFormsModule } from '@angular/forms';
import { LicenseComponent } from './license.component';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LicenseMaterialWorkspaceModule } from './material.license.workspace.module';
import { LicenseRoutingModule } from './license-routing.module';
import { LicenseCheckoutComponent } from './license-checkout/license-checkout.component';
import { LicenseReviewComponent } from './license-review/license-review.component';
import { WindowRefService } from '../services/window-ref.service';


@NgModule({
  declarations: [
    LicenseComponent,
    LicenseCheckoutComponent,
    LicenseReviewComponent
  ],
  imports: [
    CommonModule,
    LicenseMaterialWorkspaceModule,
    LicenseRoutingModule,
    ReactiveFormsModule
  ],
  exports: [
    LicenseComponent,
    LicenseCheckoutComponent,
    LicenseReviewComponent
  ],
  providers: [WindowRefService]
})
export class LicenseModule { }
