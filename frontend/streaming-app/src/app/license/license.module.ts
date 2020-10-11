import { SharedModule } from './../shared/shared.module';
import { ReactiveFormsModule } from '@angular/forms';
import { LicenseComponent } from './license.component';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LicenseMaterialWorkspaceModule } from './material.license.workspace.module';
import { CommonLicenseCheckoutComponent } from './common-license-checkout/common-license-checkout.component';
import { CommonLicenseReviewComponent } from './common-license-review/common-license-review.component';
import { WindowRefService } from '../services/window-ref.service';
import { PurchaseCommonLicenseComponent } from './purchase-common-license/purchase-common-license.component';
import { ChooseProductTypeComponent } from './choose-product-type/choose-product-type.component';
import { PurchaseStorageComponent } from './purchase-storage/purchase-storage.component';
import { PurchaseLiveClassLicenseComponent } from './purchase-live-class-license/purchase-live-class-license.component';
import { PurchaseDigitalAdaptiveExamLicenseComponent } from './purchase-digital-adaptive-exam-license/purchase-digital-adaptive-exam-license.component';
import { RetryStorageLicensePaymentComponent } from './retry-storage-license-payment/retry-storage-license-payment.component';
import { RetryCommonLicensePaymentComponent } from './retry-common-license-payment/retry-common-license-payment.component';


@NgModule({
  declarations: [
    LicenseComponent,
    CommonLicenseCheckoutComponent,
    CommonLicenseReviewComponent,
    PurchaseCommonLicenseComponent,
    ChooseProductTypeComponent,
    PurchaseStorageComponent,
    PurchaseLiveClassLicenseComponent,
    PurchaseDigitalAdaptiveExamLicenseComponent,
    RetryStorageLicensePaymentComponent,
    RetryCommonLicensePaymentComponent
  ],
  imports: [
    CommonModule,
    LicenseMaterialWorkspaceModule,
    ReactiveFormsModule,
    SharedModule
  ],
  exports: [
    LicenseComponent,
    CommonLicenseCheckoutComponent,
    CommonLicenseReviewComponent,
    PurchaseCommonLicenseComponent,
    ChooseProductTypeComponent,
    PurchaseStorageComponent,
    PurchaseLiveClassLicenseComponent,
    PurchaseDigitalAdaptiveExamLicenseComponent,
    RetryStorageLicensePaymentComponent,
    RetryCommonLicensePaymentComponent
  ],
  providers: [WindowRefService]
})
export class LicenseModule { }
