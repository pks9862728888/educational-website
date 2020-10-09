import { Router } from '@angular/router';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { UNLIMITED, INSTITUTE_TYPE_REVERSE,
         BILLING_TERM,
         BILLING_TERM_REVERSE,
         currentInstituteType,
         currentInstituteSlug,
         selectedLicenseId } from '../../../constants';
import { InstituteApiService } from '../../services/institute-api.service';
import { MediaMatcher } from '@angular/cdk/layout';
import { LicenseDetails, InstituteDiscountCouponDetailsResponse, InstituteLicenseSelectedResponse } from '../../models/license.model';
import { Component, OnInit } from '@angular/core';
import { INSTITUTE_LICENSE_PLANS } from 'src/constants';


@Component({
  selector: 'app-common-license-review',
  templateUrl: './common-license-review.component.html',
  styleUrls: ['./common-license-review.component.css']
})
export class CommonLicenseReviewComponent implements OnInit {

  mq: MediaQueryList;
  loadingText = 'Fetching License Details...';
  retryGetLicenseDetails: boolean;
  retryGetLicenseDetailsText = 'Unable to fetch license details...';
  selectedLicense: LicenseDetails;
  selectedLicenseId: string;
  currentInstituteType: string;
  currentInstituteSlug: string;
  couponCodeForm: FormGroup;
  couponError: string;
  couponApplied: string;
  couponDiscount: number;
  couponCode: string;
  amountBeforeApplyingCoupon: number;
  netPayableAmount: number;
  purchaseError: string;
  showApplyingIndicator: boolean;
  showPurchasingIndicator: boolean;

  UNLIMITED = UNLIMITED;

  constructor( private media: MediaMatcher,
               private instituteApiService: InstituteApiService,
               private formBuilder: FormBuilder,
               private router: Router ) {
    this.mq = this.media.matchMedia('(max-width: 540px)');
    this.selectedLicenseId = sessionStorage.getItem(selectedLicenseId);
    this.currentInstituteType = sessionStorage.getItem(currentInstituteType);
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
  }

  ngOnInit(): void {
    this.getLicenseDetails();
    this.couponCodeForm = this.formBuilder.group({
      coupon_code: [null, [Validators.required, Validators.minLength(6), Validators.maxLength(6)]]
    });
  }

  getLicenseDetails() {
    this.retryGetLicenseDetails = null;
    this.instituteApiService.getSelectedCommonLicenseDetails(
      sessionStorage.getItem(currentInstituteSlug),
      this.selectedLicenseId
      ).subscribe(
      (result: LicenseDetails) => {
        this.selectedLicense = result;
        if (result.billing === BILLING_TERM_REVERSE.MONTHLY) {
          const amount = Math.max(0, result.price * (1 - result.discount_percent / 100));
          this.netPayableAmount = Math.max(0, amount * (1 - result.gst_percent / 100));
        } else {
          const amount = Math.max(0, result.price * 12 * (1 - result.discount_percent / 100));
          this.netPayableAmount = Math.max(0, amount * (1 - result.gst_percent / 100));
        }
      },
      errors => {
        this.retryGetLicenseDetails = true;
      }
    );
  }

  convertToUpperCase() {
    this.couponCodeForm.patchValue({
      coupon_code: this.couponCodeForm.value.coupon_code.toUpperCase()
    });
  }

  applyCouponCode() {
    this.couponError = null;
    this.showApplyingIndicator = true;
    this.couponCode = this.couponCodeForm.value.coupon_code;
    this.instituteApiService.getDiscountCouponDetails(this.couponCode).subscribe(
      (result: InstituteDiscountCouponDetailsResponse) => {
        this.showApplyingIndicator = false;
        this.couponCodeForm.disable();
        if (result.active === true) {
          this.couponApplied = 'Coupon applied.';
          this.couponDiscount = result.discount_rs;
          this.amountBeforeApplyingCoupon = this.netPayableAmount;
          this.netPayableAmount = Math.max(0, this.netPayableAmount - this.couponDiscount);
        }
      },
      errors => {
        this.showApplyingIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.couponError = errors.error.error;
          }
        } else {
          this.couponError = 'Unable to check coupon.';
        }
      }
    );
  }

  getActivePlan(key: string) {
    return INSTITUTE_LICENSE_PLANS[key];
  }

  getBillingTerm(key: string) {
    return BILLING_TERM[key];
  }

  calculateCostInThousands(price: number, discountPercent: number) {
    return Math.max(0, (price * (1 - discountPercent / 100) / 1000)).toFixed(3);
  }

  instituteIsCollege() {
    if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE.College) {
      return true;
    } else {
      return false;
    }
  }

  hidePurchaseError() {
    this.purchaseError = null;
  }

  purchaseClicked() {
    this.showPurchasingIndicator = true;
    this.purchaseError = null;
    let code = this.couponCode;
    if (this.couponError) {
      code = '';
    }
    this.instituteApiService.purchaseCommonLicense(
      this.currentInstituteSlug,
      this.selectedLicenseId,
      code || ''
    ).subscribe(
      (result: InstituteLicenseSelectedResponse) => {
        this.showPurchasingIndicator = false;
        if (result.status === 'SUCCESS') {
          sessionStorage.setItem('netPayableAmount', result.net_amount);
          sessionStorage.setItem('selectedLicensePlanId', result.selected_license_id);
          const pathName = window.location.pathname;
          this.router.navigate([pathName.slice(0, pathName.lastIndexOf('review')) + 'checkout']);
        }
      },
      errors => {
        this.showPurchasingIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.purchaseError = errors.error.error;
          } else if (errors.error.coupon_code) {
            this.purchaseError = errors.error.coupon_code;
            this.netPayableAmount = this.amountBeforeApplyingCoupon;
            this.couponDiscount = null;
            this.couponCodeForm.enable();
            this.couponApplied = null;
            this.couponError = this.couponCode + ': ' + this.purchaseError;
            this.couponCode = null;
          } else {
            this.purchaseError = 'Unable to purchase at the moment. Please let us know.';
          }
        } else {
          this.purchaseError = 'Unable to purchase at the moment. Please let us know.';
        }
      }
    );
  }

  navigateToPurchaseCommonLicense() {
    const urlLocation = window.location.pathname;
    const loc = urlLocation.slice(0, urlLocation.length - '/review'.length);
    this.router.navigate([ loc + '/purchase-common-license' ]);
  }
}
