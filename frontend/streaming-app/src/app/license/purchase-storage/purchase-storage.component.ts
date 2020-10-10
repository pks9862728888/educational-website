import { MediaMatcher } from '@angular/cdk/layout';
import { Component, NgZone, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { postiveIntegerValidator } from 'src/app/custom.validator';
import { InstituteStorageLicenseOrderCreatedResponse,
  PaymentSuccessCallbackResponse,
         PaymentVerificatonResponse,
         StorageLicenseCredentials } from 'src/app/models/license.model';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { WindowRefService } from 'src/app/services/window-ref.service';
import { currentInstituteSlug, currentInstituteType, INSTITUTE_TYPE_REVERSE, PAYMENT_PORTAL, PAYMENT_PORTAL_REVERSE } from 'src/constants';

@Component({
  selector: 'app-purchase-storage',
  templateUrl: './purchase-storage.component.html',
  styleUrls: ['./purchase-storage.component.css']
})
export class PurchaseStorageComponent implements OnInit {

  mq: MediaQueryList;
  ref = this;
  currentInstituteSlug: string;
  currentInstituteType: string;
  pathPrefix: string;

  loadingIndicator: boolean;
  loadingError: string;
  reloadIndicator: boolean;
  payWithRazorpayIndicator: boolean;
  paymentError: string;
  paymentComplete: boolean;
  verifyPaymentIndicator: boolean;
  verificationErrorText: string;
  verificationSuccessText: string;
  retryVerification: boolean;

  purchaseForm: FormGroup;
  paymentPortalShown = false;

  storageLicenseCredentials: StorageLicenseCredentials;
  netPayableAmount: number;
  orderDetailsId: number;
  paymentPortalName: string;
  paymentSuccessCallbackResponse: PaymentSuccessCallbackResponse;

  constructor(
    private media: MediaMatcher,
    private router: Router,
    private formBuilder: FormBuilder,
    private instituteApiService: InstituteApiService,
    private windowRefService: WindowRefService,
    private ngZone: NgZone
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.currentInstituteType = sessionStorage.getItem(currentInstituteType);
    this.pathPrefix = window.location.pathname.slice(0, window.location.pathname.length - 'purchase-storage-license'.length);
  }

  ngOnInit(): void {
    this.getStorageLicenseCredentials();
    this.purchaseForm = this.formBuilder.group({
      no_of_gb: [null, [Validators.required]],
      months: [1, [Validators.required, postiveIntegerValidator]]
    });
  }

  getStorageLicenseCredentials() {
    this.loadingIndicator = true;
    this.loadingError = null;
    this.reloadIndicator = false;
    this.instituteApiService.getStorageLicenseCredentials(
      this.currentInstituteSlug
    ).subscribe(
      (result: StorageLicenseCredentials) => {
        this.storageLicenseCredentials = result;
        this.updatePurchaseForm();
        this.loadingIndicator = false;
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

  updatePurchaseForm() {
    this.purchaseForm.patchValue({
      no_of_gb: this.storageLicenseCredentials.min_storage,
      months: 1
    });
  }

  showPaymentPortal() {
    this.purchaseForm.disable();
    this.paymentPortalShown = true;
  }

  createOrder(paymentGatewayName: string) {
    const data = this.purchaseForm.value;
    data.payment_gateway = PAYMENT_PORTAL_REVERSE[paymentGatewayName];
    this.payWithRazorpayIndicator = true;
    this.paymentError = null;
    this.instituteApiService.createStorageLicenseOrder(
      this.currentInstituteSlug,
      data
    ).subscribe(
      (result: InstituteStorageLicenseOrderCreatedResponse) => {
        this.payWithRazorpayIndicator = false;
        console.log(result);
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
      this.instituteApiService.sendStorageLicenseCallbackAndVerifyPayment(
        response,
        this.orderDetailsId.toString()
        ).subscribe(
        (result: PaymentVerificatonResponse) => {
          this.verifyPaymentIndicator = false;
          if (result.status === 'SUCCESS') {
            this.verificationSuccessText = 'Payment is successful. Redirecting...';
            setTimeout(() => {
              this.ngZone.run(() => this.redirectToLicenseView());
            }, 2000);
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

  retryVerificationClicked() {
    if (this.paymentPortalName === 'RAZORPAY') {
      this.razorpayCallbackFunction(this.paymentSuccessCallbackResponse);
    }
  }

  payWithRazorpay(data: InstituteStorageLicenseOrderCreatedResponse, ref: any) {
    const options = {
      key: data.key_id,
      amount: data.amount,
      currency: data.currency,
      name: 'Scholar Diet',
      description: 'Purchasing institute storage license @' + data.no_of_gb.toString() + ' GB for ' + data.months.toString() + ' months.',
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

  calculateCostBeforeTax() {
    const data = this.purchaseForm.value;
    return (this.storageLicenseCredentials.price * data.no_of_gb * data.months * 30).toFixed(3);
  }

  calculateNetPayableAmount() {
    const data = this.purchaseForm.value;
    this.netPayableAmount = this.storageLicenseCredentials.price * data.no_of_gb * data.months * 30 * (1 +
      this.storageLicenseCredentials.gst_percent / 100);
    return this.netPayableAmount.toFixed(3);
  }

  navigateToChooseProductType() {
    this.router.navigate([ this.pathPrefix + 'choose-product-type']);
  }

}
