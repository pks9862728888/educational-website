import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LicenseComponent } from '../license/license.component';
import { ChooseProductTypeComponent } from './choose-product-type/choose-product-type.component';
import { CommonLicenseCheckoutComponent } from './common-license-checkout/common-license-checkout.component';
import { CommonLicenseReviewComponent } from './common-license-review/common-license-review.component';
import { PurchaseCommonLicenseComponent } from './purchase-common-license/purchase-common-license.component';
import { PurchaseDigitalAdaptiveExamLicenseComponent } from './purchase-digital-adaptive-exam-license/purchase-digital-adaptive-exam-license.component';
import { PurchaseLiveClassLicenseComponent } from './purchase-live-class-license/purchase-live-class-license.component';
import { PurchaseStorageComponent } from './purchase-storage/purchase-storage.component';
import { RetryCommonLicensePaymentComponent } from './retry-common-license-payment/retry-common-license-payment.component';
import { RetryStorageLicensePaymentComponent } from './retry-storage-license-payment/retry-storage-license-payment.component';

const routes: Routes = [
  {
    path: '',
    component: LicenseComponent,
    children: [
      { path: 'retry-storage-license-payment/:order_id', component: RetryStorageLicensePaymentComponent },
      { path: 'retry-common-license-payment/:order_id', component: RetryCommonLicensePaymentComponent },
      { path: 'choose-product-type', component: ChooseProductTypeComponent },
      { path: 'purchase-common-license', component: PurchaseCommonLicenseComponent},
      { path: 'purchase-storage-license', component: PurchaseStorageComponent},
      { path: 'purchase-digital-adaptive-exam-license', component: PurchaseDigitalAdaptiveExamLicenseComponent},
      { path: 'purchase-live-class-license', component: PurchaseLiveClassLicenseComponent},
      { path: 'review', component: CommonLicenseReviewComponent},
      { path: 'checkout', component: CommonLicenseCheckoutComponent }
    ],
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  providers: [
  ]
})
export class LicenseRoutingModule {}

export const licenseRoutingComponents = [
  LicenseComponent,
  RetryStorageLicensePaymentComponent,
  RetryCommonLicensePaymentComponent,
  ChooseProductTypeComponent,
  PurchaseCommonLicenseComponent,
  PurchaseStorageComponent,
  PurchaseDigitalAdaptiveExamLicenseComponent,
  PurchaseLiveClassLicenseComponent,
  CommonLicenseReviewComponent,
  CommonLicenseCheckoutComponent
];
