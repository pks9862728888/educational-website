import { PAYMENT_PORTAL_REVERSE } from './../../../constants';
import { InstituteApiService } from 'src/app/institute-api.service';
import { Component, OnInit } from '@angular/core';
import { InstituteLicenceOrderCreatedResponse } from '../license.model';
import { MediaMatcher } from '@angular/cdk/layout';

@Component({
  selector: 'app-license-checkout',
  templateUrl: './license-checkout.component.html',
  styleUrls: ['./license-checkout.component.css']
})
export class LicenseCheckoutComponent implements OnInit {

  mobileQuery: MediaQueryList;
  createOrderError: string;
  currentInstituteSlug: string;
  selectedLicensePlanId: string;
  netPayableAmount: string;
  showInitiatingPaymentIndicator: boolean;

  constructor( private media: MediaMatcher,
               private instituteApiService: InstituteApiService ) {
    this.mobileQuery = this.media.matchMedia('(max-width: 540px)');
    this.currentInstituteSlug = sessionStorage.getItem('currentInstituteSlug');
    this.selectedLicensePlanId = sessionStorage.getItem('selectedLicensePlanId');
    this.netPayableAmount = sessionStorage.getItem('netPayableAmount');
  }

  ngOnInit(): void {}

  createOrder(paymentPortalName: string) {
    this.showInitiatingPaymentIndicator = true;
    this.instituteApiService.createOrder(
      this.currentInstituteSlug,
      this.selectedLicensePlanId,
      PAYMENT_PORTAL_REVERSE[paymentPortalName]).subscribe(
        (result: InstituteLicenceOrderCreatedResponse) => {
          this.showInitiatingPaymentIndicator = false;
          if (result.status === 'SUCCESS') {
            console.log(result);
          }
        },
        errors => {
          this.showInitiatingPaymentIndicator = false;
          if (errors.error) {
            if (errors.error.error) {
              this.createOrderError = errors.error.error;
            } else {
              this.createOrderError = 'Unable to process request. Please try again after sometime.';
            }
          } else {
            this.createOrderError = 'Unable to process request. Check internet connectivity.';
          }
        }
      )
  }

  hideCreateOrderError() {
    this.createOrderError = null;
  }

}
