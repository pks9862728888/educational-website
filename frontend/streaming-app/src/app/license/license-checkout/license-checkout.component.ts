import { INSTITUTE_LICENSE_PLANS } from 'src/constants';
import { WindowRefService } from './../../services/window-ref.service';
import { PAYMENT_PORTAL_REVERSE, INSTITUTE_TYPE_REVERSE } from './../../../constants';
import { InstituteApiService } from '../../services/institute-api.service';
import { Component, OnInit, NgZone } from '@angular/core';
import { InstituteLicenceOrderCreatedResponse, PaymentSuccessCallbackResponse, PaymentVerificatonResponse } from '../license.model';
import { MediaMatcher } from '@angular/cdk/layout';
import { Router } from '@angular/router';

@Component({
  selector: 'app-license-checkout',
  templateUrl: './license-checkout.component.html',
  styleUrls: ['./license-checkout.component.css']
})
export class LicenseCheckoutComponent implements OnInit {

  mobileQuery: MediaQueryList;
  currentInstituteSlug: string;
  currentInstituteType: string;
  errorText: string;
  successText: string;
  selectedLicensePlanId: string;
  netPayableAmount: string;
  orderDetailsId: string;
  paymentPortalName: string;
  initiatingPaymentIndicator: boolean;
  paymentSuccessCallbackResponse: PaymentSuccessCallbackResponse;
  verifyPaymentIndicator: boolean;
  paymentComplete: boolean;
  retryVerification: boolean;
  ref = this;

  constructor( private media: MediaMatcher,
               private router: Router,
               private instituteApiService: InstituteApiService,
               private windowRefService: WindowRefService,
               private ngZone: NgZone ) {
    this.mobileQuery = this.media.matchMedia('(max-width: 540px)');
    this.currentInstituteSlug = sessionStorage.getItem('currentInstituteSlug');
    this.currentInstituteType = sessionStorage.getItem('currentInstituteType');
    this.selectedLicensePlanId = sessionStorage.getItem('selectedLicensePlanId');
    this.netPayableAmount = sessionStorage.getItem('netPayableAmount');
  }

  ngOnInit(): void {
    if (sessionStorage.getItem('paymentComplete')) {
      sessionStorage.removeItem('paymentComplete');
      this.redirectToLicenseView();
    }
  }

  createOrder(paymentPortalName: string) {
    this.paymentPortalName = paymentPortalName;
    this.initiatingPaymentIndicator = true;
    this.errorText = null;
    this.instituteApiService.createOrder(
      this.currentInstituteSlug,
      this.selectedLicensePlanId,
      PAYMENT_PORTAL_REVERSE[paymentPortalName]).subscribe(
        (result: InstituteLicenceOrderCreatedResponse) => {
          this.initiatingPaymentIndicator = false;
          if (result.status === 'SUCCESS') {
            this.orderDetailsId = result.order_details_id;
            this.payWithRazorpay(result, this.ref);
          }
        },
        errors => {
          this.initiatingPaymentIndicator = false;
          if (errors.error) {
            if (errors.error.error) {
              this.errorText = errors.error.error;
            } else {
              this.errorText = 'Unable to process request. Please try again after sometime.';
            }
          } else {
            this.errorText = 'Unable to process request. Check internet connectivity.';
          }
        }
      )
  }

  razorpayCallbackFunction(response: PaymentSuccessCallbackResponse) {
    this.ngZone.run(() => {
      this.paymentComplete = true;
      this.verifyPaymentIndicator = true;
      this.errorText = null;
      this.successText = null;
      this.retryVerification = false;
      this.instituteApiService.sendCallbackAndVerifyPayment(response, this.orderDetailsId).subscribe(
        (result: PaymentVerificatonResponse) => {
          this.verifyPaymentIndicator = false;
          if (result.status === 'SUCCESS') {
            this.successText = 'Payment is successful. Redirecting...';
            setTimeout(() => {
              this.ngZone.run(() => this.redirectToLicenseView());
            }, 2000);
          } else {
            this.errorText = 'Payment verification failed. You can retry payment if money was not deducted. If money was deducted please let us know.';
          }
        },
        errors => {
          this.verifyPaymentIndicator = false;
          if (errors.error) {
            this.errorText = errors.error;
          }
          this.errorText = 'Payment verification error. If payment was successful, then we will verify it automatically after sometime.'
          this.retryVerification = true;
        }
      )
    });
  }

  payWithRazorpay(data: InstituteLicenceOrderCreatedResponse, ref: any) {
    const options = {
      "key": data.key_id,
      "amount": data.amount,
      "currency": data.currency,
      "name": "Edu Web",
      "description": "Purchasing institute " + INSTITUTE_LICENSE_PLANS[data.type].toLowerCase() + " license.",
      "image": "",
      "order_id": data.order_id,
      "handler": function(response: PaymentSuccessCallbackResponse){
        ref.paymentSuccessCallbackResponse = response;
        sessionStorage.setItem('paymentComplete', 'true');
        ref.razorpayCallbackFunction(response);
      },
      "prefill": {
        "email": data.email,
        "contact": data.contact || ''
      },
      "notes": {},
      "theme": {
          "color": "#4CC5E4"
      }
    };

    const rzpWindow = new this.windowRefService.nativeWindow.Razorpay(options);
    rzpWindow.open();
  }

  redirectToLicenseView() {
    if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE['School']) {
      this.router.navigate(['/school-workspace/' + this.currentInstituteSlug + '/license']);
    } else if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE['College']) {
      this.router.navigate(['/college-workspace/' + this.currentInstituteSlug + '/license']);
    } else if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE['Coaching']) {
      this.router.navigate(['/coaching-workspace/' + this.currentInstituteSlug + '/license']);
    }
  }

  retryVerificationClicked() {
    if (this.paymentPortalName === 'RAZORPAY') {
      this.razorpayCallbackFunction(this.paymentSuccessCallbackResponse);
    }
  }

  hideErrorText() {
    this.errorText = null;
  }
}
