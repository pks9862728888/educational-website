import { InAppDataTransferService } from './../services/in-app-data-transfer.service';
import { INSTITUTE_LICENSE_PLANS,
         BILLING_TERM, UNLIMITED,
         purchasedLicenseExists,
         paymentComplete, PRODUCT_TYPES, INSTITUTE_LICENSE_PLANS_REVERSE, BILLING_TERM_REVERSE } from './../../constants';
import { Router } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { InstituteApiService } from '../services/institute-api.service';
import { LicenseOrderResponse,
         ActiveLicenseDetails,
         ExpiredLicenseDetails, LicenseDetails } from '../models/license.model';
import { getDateFromUnixTimeStamp } from '../format-datepicker';
import { UiService } from '../services/ui.service';
import { isInstituteCollege } from '../shared/utilityFunctions';


@Component({
  selector: 'app-license',
  templateUrl: './license.component.html',
  styleUrls: ['./license.component.css']
})
export class LicenseComponent implements OnInit {

  mq: MediaQueryList;
  currentInstituteSlug: string;

  UNLIMITED = UNLIMITED;
  PRODUCT_TYPES = PRODUCT_TYPES;
  INSTITUTE_LICENSE_PLANS_REVERSE = INSTITUTE_LICENSE_PLANS_REVERSE;
  INSTITUTE_LICENSE_PLANS = INSTITUTE_LICENSE_PLANS;
  BILLING_TERM = BILLING_TERM;
  getDateFromUnixTimeStamp = getDateFromUnixTimeStamp;
  isInstituteCollege = isInstituteCollege;

  openedProductStep: number;
  openedLicenseTypeStep: number;
  openedLicensePlanStep: number;
  productTypes = [
    'LMS + CMS + Digital Exam Licenses',
    'Storage'
  ];

  licenseOrdersLoading: boolean;
  licenseOrdersError: string;
  licenseOrdersReload: boolean;
  loadingLicensePlanDetails: boolean;

  licenseData: LicenseOrderResponse;
  commonLicensePlanDetails: LicenseDetails;

  constructor(
    private media: MediaMatcher,
    private router: Router,
    private instituteApiService: InstituteApiService,
    private inAppDataTransferService: InAppDataTransferService,
    private uiService: UiService
    ) {
    this.mq = this.media.matchMedia('(max-width: 540px)');
    this.currentInstituteSlug = sessionStorage.getItem('currentInstituteSlug');
  }

  ngOnInit() {}

  fetchLicenseDetails(step: number) {
    let licenseType: string;

    if (step === 0) {
      licenseType = PRODUCT_TYPES.LMS_CMS_EXAM_LIVE_STREAM;
    } else if (step === 1) {
      licenseType = PRODUCT_TYPES.STORAGE;
    }

    this.licenseOrdersLoading = true;
    this.licenseOrdersReload = false;
    this.licenseOrdersError = null;

    this.instituteApiService.getInstituteOrderedLicense(
      this.currentInstituteSlug,
      licenseType
      ).subscribe(
      (result: LicenseOrderResponse) => {
        this.licenseOrdersLoading = false;
        this.licenseData = result;
        console.log(result);
      },
      errors => {
        this.licenseOrdersLoading = false;
        if (errors.error) {
          if (errors.error.error) {
            this.licenseOrdersError = errors.error.error;
          } else {
            this.licenseOrdersReload = true;
          }
        } else {
          this.licenseOrdersReload = true;
        }
      }
    );
  }

  loadMoreCommonLicenseDetails(selectedLicenseId: number) {
    this.loadingLicensePlanDetails = true;
    this.instituteApiService.getOrderedCommonLicenseDetails(
      this.currentInstituteSlug,
      selectedLicenseId.toString()
    ).subscribe(
      (result: LicenseDetails) => {
        this.loadingLicensePlanDetails = false;
        console.log(result);
        this.commonLicensePlanDetails = result;
      },
      errors => {
        this.loadingLicensePlanDetails = false;
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(
              errors.error.error,
              3000
            );
          } else {
            this.uiService.showSnackBar(
              'Error! Unable to load license plan details at the moment.',
              3000
            );
          }
        } else {
          this.uiService.showSnackBar(
            'Error! Unable to load license plan details at the moment.',
            3000
          );
        }
      }
    );
  }

  setOpenedProductStep(step: number) {
    this.openedLicenseTypeStep = null;
    this.openedLicensePlanStep = null;
    this.commonLicensePlanDetails = null;
    this.loadingLicensePlanDetails = false;

    if (step === this.openedProductStep) {
      this.openedProductStep = null;
      this.licenseOrdersLoading = false;
      this.licenseOrdersError = null;
      this.licenseOrdersReload = false;
    } else {
      this.openedProductStep = step;
      this.fetchLicenseDetails(step);
    }
  }

  setOpenedLicenseTypeStep(step: number) {
    this.openedLicensePlanStep = null;
    this.loadingLicensePlanDetails = false;
    this.commonLicensePlanDetails = null;

    if (step === this.openedLicenseTypeStep) {
      this.openedLicenseTypeStep = null;
    } else {
      let type: string;
      if (step === 0) {
        type = 'active_license';
      } else if (step === 1) {
        type = 'expired_license';
      } else {
        type = 'pending_payment_license';
      }
      if (this.licenseData[type].length > 0) {
        this.openedLicenseTypeStep = step;
      }
    }
  }

  setOpenedLicensePlanStep(step: number) {
    this.loadingLicensePlanDetails = false;
    this.commonLicensePlanDetails = null;

    if (step === this.openedLicensePlanStep) {
      this.openedLicensePlanStep = null;
    } else {
      this.openedLicensePlanStep = step;
    }
  }

  purchaseLicense() {
    this.router.navigate([window.location.pathname + '/choose-product-type']);
  }
}
