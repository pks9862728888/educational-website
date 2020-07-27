import { Router } from '@angular/router';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { UNLIMITED, INSTITUTE_TYPE_REVERSE, DISCUSSION_FORUM_PER_ATTENDEES, BILLING_TERM, BILLING_TERM_REVERSE } from './../../../constants';
import { InstituteApiService } from './../../institute-api.service';
import { MediaMatcher } from '@angular/cdk/layout';
import { LicenseDetails, InstituteDiscountCouponDetailsResponse, InstituteLicenseSelectedResponse } from './../license.model';
import { Component, OnInit } from '@angular/core';
import { INSTITUTE_LICENSE_PLANS } from 'src/constants';


@Component({
  selector: 'app-license-review',
  templateUrl: './license-review.component.html',
  styleUrls: ['./license-review.component.css']
})
export class LicenseReviewComponent implements OnInit {

  mobileQuery: MediaQueryList;
  retryGetLicenseDetails: boolean;
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
    this.mobileQuery = this.media.matchMedia('(max-width: 540px)');
    this.selectedLicenseId = sessionStorage.getItem('selectedLicenseId');
  }

  ngOnInit(): void {
    this.getLicenseDetails();
    this.couponCodeForm = this.formBuilder.group({
      coupon_code: [null, [Validators.required, Validators.minLength(6), Validators.maxLength(6)]]
    });
    this.currentInstituteType = sessionStorage.getItem('currentInstituteType');
    this.currentInstituteSlug = sessionStorage.getItem('currentInstituteSlug');
  }

  getLicenseDetails() {
    this.retryGetLicenseDetails = null;
    this.instituteApiService.getSelectedLicenseDetails(this.selectedLicenseId).subscribe(
      (result: LicenseDetails) => {
        this.selectedLicense = result;
        if (result.billing === BILLING_TERM_REVERSE['MONTHLY']) {
          this.netPayableAmount = Math.max(0, result.amount * (1 - result.discount_percent/100));
        } else {
          this.netPayableAmount = Math.max(0, result.amount * 12 * (1 - result.discount_percent/100));
        }
      },
      errors => {
        this.retryGetLicenseDetails = true;
      }
    )
  }

  convertToUpperCase() {
    this.couponCodeForm.patchValue({
      'coupon_code': this.couponCodeForm.value['coupon_code'].toUpperCase()
    });
  }

  applyCouponCode() {
    this.couponError = null;
    this.showApplyingIndicator = true;
    this.couponCode = this.couponCodeForm.value['coupon_code'];
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
    )
  }

  getActivePlan(key: string) {
    return INSTITUTE_LICENSE_PLANS[key];
  }

  getBillingTerm(key: string) {
    return BILLING_TERM[key];
  }

  getDiscussionForums(key: string) {
    return DISCUSSION_FORUM_PER_ATTENDEES[key];
  }

  calculateCostInThousands(amount:number, discountPercent: number) {
    return Math.max(0, (amount * (1 - discountPercent/100))/1000);
  }

  instituteIsCoaching() {
    if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE['Coaching']) {
      return true
    } else {
      return false
    }
  }

  changeLicense() {
    sessionStorage.removeItem('selectedLicenseId');
    this.navigateToWorkspace('/license');
  }

  navigateToWorkspace(path: string) {
    if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE['School']) {
      this.router.navigate(['/school-workspace/' + this.currentInstituteSlug + path]);
    } else if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE['Coaching']) {
      this.router.navigate(['/coaching-workspace/' + this.currentInstituteSlug + path]);
    } else if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE['College']) {
      this.router.navigate(['/college-workspace/' + this.currentInstituteSlug + path]);
    }
  }

  hideCouponError() {
    this.couponError = null;
  }

  hidePurchaseError() {
    this.purchaseError = null;
  }

  purchaseClicked() {
    this.showPurchasingIndicator = true;
    this.purchaseError = null;
    this.instituteApiService.purchase(
      this.currentInstituteSlug,
      this.selectedLicenseId,
      this.couponCode || ''
    ).subscribe(
      (result: InstituteLicenseSelectedResponse) => {
        this.showPurchasingIndicator = false;
        if (result.status === 'SUCCESS') {
          sessionStorage.setItem('netPayableAmount', result.net_amount);
          sessionStorage.setItem('selectedLicensePlanId', result.selected_license_id);
          this.navigateToWorkspace('/license/checkout');
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
          }
        } else {
          this.purchaseError = 'Unable to purchase at the moment. Please let us know.';
        }
      }
    )
  }
}
