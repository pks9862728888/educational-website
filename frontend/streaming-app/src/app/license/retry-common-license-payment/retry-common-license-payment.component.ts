import { MediaMatcher } from '@angular/cdk/layout';
import { Component, NgZone, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { getDateFromUnixTimeStamp } from 'src/app/format-datepicker';
import { CommonLicenseOrderCredentialsForRetryPayment, InstituteLicenseOrderCreatedResponse, PaymentSuccessCallbackResponse, PaymentVerificatonResponse } from 'src/app/models/license.model';
import { InAppDataTransferService } from 'src/app/services/in-app-data-transfer.service';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { UiService } from 'src/app/services/ui.service';
import { WindowRefService } from 'src/app/services/window-ref.service';
import { BILLING_TERM,
  BILLING_TERM_REVERSE,
         currentInstituteSlug,
         currentInstituteType,
         INSTITUTE_LICENSE_PLANS,
         INSTITUTE_LICENSE_PLANS_REVERSE,
         INSTITUTE_TYPE_REVERSE,
         PAYMENT_PORTAL_REVERSE,
         UNLIMITED} from 'src/constants';

@Component({
  selector: 'app-retry-common-license-payment',
  templateUrl: './retry-common-license-payment.component.html',
  styleUrls: ['./retry-common-license-payment.component.css']
})
export class RetryCommonLicensePaymentComponent implements OnInit {

  mq: MediaQueryList;
  currentInstituteSlug: string;
  currentInstituteType: string;
  ref = this;

  loadingIndicator: boolean;
  loadingError: string;
  reloadIndicator: boolean;
  paymentComplete: boolean;
  payWithRazorpayIndicator: boolean;
  paymentError: string;
  verifyPaymentIndicator: boolean;
  verificationErrorText: string;
  verificationSuccessText: string;
  retryVerification: boolean;

  UNLIMITED = UNLIMITED;
  BILLING_TERM = BILLING_TERM;
  INSTITUTE_LICENSE_PLANS_REVERSE = INSTITUTE_LICENSE_PLANS_REVERSE;
  INSTITUTE_LICENSE_PLANS = INSTITUTE_LICENSE_PLANS;
  getDateFromUnixTimeStamp = getDateFromUnixTimeStamp;

  orderId: string;
  orderCredentials: CommonLicenseOrderCredentialsForRetryPayment;
  orderDetailsId: string;
  paymentPortalName: string;
  paymentSuccessCallbackResponse: PaymentSuccessCallbackResponse;

  constructor(
    private media: MediaMatcher,
    private router: Router,
    private instituteApiService: InstituteApiService,
    private inAppDataTransferService: InAppDataTransferService,
    private windowRefService: WindowRefService,
    private uiService: UiService,
    private ngZone: NgZone
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.currentInstituteType = sessionStorage.getItem(currentInstituteType);
    const paths = window.location.pathname.split('/');
    this.orderId = paths[paths.length - 1];
  }

  ngOnInit(): void {
    this.getLicenseOrderDetails();
  }

  getLicenseOrderDetails() {
    this.loadingIndicator = true;
    this.loadingError = null;
    this.reloadIndicator = false;
    this.instituteApiService.getCommonLicenseCredentialsForRetryPayment(
      this.currentInstituteSlug,
      this.orderId
    ).subscribe(
      (result: CommonLicenseOrderCredentialsForRetryPayment) => {
        this.loadingIndicator = false;
        console.log(result);
        this.orderCredentials = result;
      },
      errors => {
        this.loadingIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.loadingError = errors.error.error;
          } else {
            this.reloadIndicator = true;
          }
        } else {
          this.reloadIndicator = true;
        }
      }
    );
  }

  createOrder(paymentGatewayName: string) {
    this.payWithRazorpayIndicator = true;
    this.paymentError = null;
    this.instituteApiService.createCommonLicenseOrder(
      this.currentInstituteSlug,
      this.orderCredentials.selected_license_id.toString(),
      PAYMENT_PORTAL_REVERSE[paymentGatewayName]
    ).subscribe(
      (result: InstituteLicenseOrderCreatedResponse) => {
        this.payWithRazorpayIndicator = false;
        if (result.status === 'SUCCESS') {
          this.orderDetailsId = result.order_details_id;
          this.paymentPortalName = paymentGatewayName;
          this.payWithRazorpay(result, this.ref);
        }
      },
      errors => {
        this.payWithRazorpayIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.paymentError = errors.error.error;
          } else {
            this.paymentError = 'Error. Unable to generate payment id. Please try again.';
          }
        } else {
          this.paymentError = 'Error. Unable to generate payment id. Please try again.';
        }
      }
    );
  }

  razorpayCallbackFunction(response: PaymentSuccessCallbackResponse) {
    this.ngZone.run(() => {
      this.paymentComplete = true;
      this.verifyPaymentIndicator = true;
      this.verificationErrorText = null;
      this.verificationSuccessText = null;
      this.retryVerification = false;
      this.instituteApiService.sendCommonLicensePurchaseCallbackAndVerifyPayment(
        response,
        this.orderDetailsId
        ).subscribe(
        (result: PaymentVerificatonResponse) => {
          this.verifyPaymentIndicator = false;
          if (result.status === 'SUCCESS') {
            this.verificationSuccessText = 'Payment is successful. Redirecting...';
            setTimeout(() => {
              this.ngZone.run(() => this.redirectToLicenseView());
            }, 2000);
            this.inAppDataTransferService.showTeacherLmsCmsInstituteView();
          } else {
            this.verificationErrorText = 'Payment verification failed. You can retry payment if money was not deducted. If money was deducted please let us know.';
          }
        },
        errors => {
          this.verifyPaymentIndicator = false;
          if (errors.error) {
            if (errors.error.error) {
              this.verificationErrorText = errors.error.error;
            } else {
              this.verificationErrorText = 'Payment verification error.' +
              ' If payment was successful, then we will verify it automatically after sometime.';
            }
          } else {
            this.verificationErrorText = 'Payment verification error. If payment was successful, then we will verify it automatically after sometime.';
          }
          this.retryVerification = true;
        }
      );
    });
  }

  payWithRazorpay(data: InstituteLicenseOrderCreatedResponse, ref: any) {
    const options = {
      key: data.key_id,
      amount: data.amount,
      currency: data.currency,
      name: 'Scholar Diet',
      description: 'Purchasing institute ' + INSTITUTE_LICENSE_PLANS[data.type].toLowerCase() + ' license.',
      image: '',
      order_id: data.order_id,
      // tslint:disable-next-line: object-literal-shorthand && only-arrow-functions
      handler: function(response: PaymentSuccessCallbackResponse){
        ref.paymentSuccessCallbackResponse = response;
        ref.razorpayCallbackFunction(response);
      },
      prefill: {
        email: data.email,
        contact: data.contact || ''
      },
      notes: {},
      theme: {
          color: '#4CC5E4'
      }
    };

    const rzpWindow = new this.windowRefService.nativeWindow.Razorpay(options);
    rzpWindow.open();
  }

  redirectToLicenseView() {
    if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE.School) {
      this.router.navigate(['/school-workspace/' + this.currentInstituteSlug + '/license']);
    } else if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE.College) {
      this.router.navigate(['/college-workspace/' + this.currentInstituteSlug + '/license']);
    } else if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE.Coaching) {
      this.router.navigate(['/coaching-workspace/' + this.currentInstituteSlug + '/license']);
    }
  }

  retryVerificationClicked() {
    if (this.paymentPortalName === 'RAZORPAY') {
      this.razorpayCallbackFunction(this.paymentSuccessCallbackResponse);
    }
  }

  calculateAmountWithoutTax() {
    const price = this.orderCredentials.price;
    let month = 1;
    let discountRs = 0;

    if (this.orderCredentials.billing === BILLING_TERM_REVERSE.ANNUALLY) {
      month = 12;
    }

    if (this.orderCredentials.discount_rs) {
      discountRs = this.orderCredentials.discount_rs;
    }

    return (price * month * ( 1 - this.orderCredentials.discount_percent / 100) - discountRs).toFixed(3);
  }

  navigateToLicenseList() {
    const pathUrl = window.location.pathname;
    const lengthToSubtract = '/retry-common-license-payment/'.length + this.orderId.length;
    this.router.navigate([ pathUrl.slice(0, pathUrl.length - lengthToSubtract ) ]);
  }

  isInstituteCollege() {
    if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE.College) {
      return true;
    } else {
      return false;
    }
  }

}
