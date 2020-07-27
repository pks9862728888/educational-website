import { INSTITUTE_LICENSE_PLANS } from 'src/constants';
import { WindowRefService } from './../../services/window-ref.service';
import { PAYMENT_PORTAL_REVERSE } from './../../../constants';
import { InstituteApiService } from 'src/app/institute-api.service';
import { Component, OnInit } from '@angular/core';
import { InstituteLicenceOrderCreatedResponse, PaymentSuccessCallbackResponse, PaymentVerificatonResponse } from '../license.model';
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
  orderDetailsId: string;
  showInitiatingPaymentIndicator: boolean;
  paymentSuccessCallbackResponse: PaymentSuccessCallbackResponse;
  ref = this;

  constructor( private media: MediaMatcher,
               private instituteApiService: InstituteApiService,
               private windowRefService: WindowRefService ) {
    this.mobileQuery = this.media.matchMedia('(max-width: 540px)');
    this.currentInstituteSlug = sessionStorage.getItem('currentInstituteSlug');
    this.selectedLicensePlanId = sessionStorage.getItem('selectedLicensePlanId');
    this.netPayableAmount = sessionStorage.getItem('netPayableAmount');
  }

  ngOnInit(): void {}

  createOrder(paymentPortalName: string) {
    this.showInitiatingPaymentIndicator = true;
    this.createOrderError = null;
    this.instituteApiService.createOrder(
      this.currentInstituteSlug,
      this.selectedLicensePlanId,
      PAYMENT_PORTAL_REVERSE[paymentPortalName]).subscribe(
        (result: InstituteLicenceOrderCreatedResponse) => {
          this.showInitiatingPaymentIndicator = false;
          if (result.status === 'SUCCESS') {
            this.orderDetailsId = result.order_details_id;
            this.payWithRazorpay(result, this.ref);
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

  razorpayCallbackFunction(response: PaymentSuccessCallbackResponse) {
    this.instituteApiService.sendCallbackAndVerifyPayment(response, this.orderDetailsId).subscribe(
      (result: PaymentVerificatonResponse) => {
        if (result.status === 'SUCCESS') {
          console.log(result.status);
        } else {
          console.log(result.status);
        }
      }
    )
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

  hideCreateOrderError() {
    this.createOrderError = null;
  }

}
