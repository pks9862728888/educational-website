import { InAppDataTransferService } from './../services/in-app-data-transfer.service';
import { INSTITUTE_LICENSE_PLANS,
         BILLING_TERM, UNLIMITED,
         PRODUCT_TYPES,
         INSTITUTE_LICENSE_PLANS_REVERSE,
         BILLING_TERM_REVERSE } from './../../constants';
import { Router } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { InstituteApiService } from '../services/institute-api.service';
import { LicenseOrderResponse,
         LicenseDetails } from '../models/license.model';
import { getDateFromUnixTimeStamp } from '../format-datepicker';
import { UiService } from '../services/ui.service';
import { isInstituteCollege } from '../shared/utilityFunctions';
import { MatDialog } from '@angular/material/dialog';
import { UiDialogComponent } from '../shared/ui-dialog/ui-dialog.component';


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
  deleteIndicator: boolean;

  licenseData: LicenseOrderResponse;
  commonLicensePlanDetails: LicenseDetails;

  constructor(
    private media: MediaMatcher,
    private router: Router,
    private instituteApiService: InstituteApiService,
    private inAppDataTransferService: InAppDataTransferService,
    private uiService: UiService,
    public dialog: MatDialog
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
    this.deleteIndicator = false;

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
    this.loadingLicensePlanDetails = false;
    this.commonLicensePlanDetails = null;
    this.deleteIndicator = false;

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
        this.openedLicensePlanStep = null;
      }
    }
  }

  setOpenedLicensePlanStep(step: number) {
    this.loadingLicensePlanDetails = false;
    this.commonLicensePlanDetails = null;
    this.deleteIndicator = false;

    if (step === this.openedLicensePlanStep) {
      this.openedLicensePlanStep = null;
    } else {
      this.openedLicensePlanStep = step;
    }
  }

  durationMoreThanThreeDays(orderCreationTimeStamp: number) {
    if (+new Date() - orderCreationTimeStamp > 86400 * 1000 * 3) {
      return true;
    } else {
      return false;
    }
  }

  confirmDeleteUnpaidLicense(lic, productTypeIndex: number) {
    let titleText: string;

    if (productTypeIndex === 0) {
      titleText = INSTITUTE_LICENSE_PLANS[lic.type].toUpperCase() + ' billed ' + BILLING_TERM_REVERSE[lic.billing];
    } else if (productTypeIndex === 1) {
      titleText = lic.no_of_gb + 'GB @' + lic.months + ' months';
    }

    const dialogRef = this.dialog.open(UiDialogComponent, {
      data: {
        title: 'Do you want to delete unpaid license "' + titleText + '"? No issues can be raised about it later.',
        trueStringDisplay: 'Yes',
        falseStringDisplay: 'No'
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        if (productTypeIndex === 0) {
          this.deleteCommonLicense(lic);
        } else if (productTypeIndex === 1) {
          this.deleteStorageLicense(lic);
        }
      }
    });
  }

  deleteCommonLicense(lic) {
    this.deleteIndicator = true;
    this.instituteApiService.deleteUnpaidCommonLicense(
      this.currentInstituteSlug,
      lic.order_pk.toString()
    ).subscribe(
      () => {
        this.deleteIndicator = false;
        let idx = -1;

        for (const i in this.licenseData.pending_payment_license) {
          if (this.licenseData.pending_payment_license[i].order_pk === lic.order_pk) {
            idx = +i;
            break;
          }
        }

        this.licenseData.pending_payment_license.splice(idx, 1);
        this.uiService.showSnackBar(
          'Unpaid license deleted successfully!',
          3000
        );
      },
      errors => {
        this.deleteIndicator = false;
        if (errors.errors) {
          if (errors.errors.error) {
            this.uiService.showSnackBar(
              errors.error.error,
              3000
            );
          } else {
            this.uiService.showSnackBar(
              'Error occured! Unable to delete unpaid common license at the moment.',
              3000
            );
          }
        } else {
          this.uiService.showSnackBar(
            'Error occured! Unable to delete unpaid common license at the moment.',
            3000
          );
        }
      }
    );
  }

  deleteStorageLicense(lic) {
    this.deleteIndicator = true;
    this.instituteApiService.deleteUnpaidStorageLicense(
      this.currentInstituteSlug,
      lic.order_pk.toString()
    ).subscribe(
      () => {
        this.deleteIndicator = false;
        let idx = -1;

        for (const i in this.licenseData.pending_payment_license) {
          if (this.licenseData.pending_payment_license[i].order_pk === lic.order_pk) {
            idx = +i;
            break;
          }
        }

        this.licenseData.pending_payment_license.splice(idx, 1);
        this.uiService.showSnackBar(
          'Unpaid license deleted successfully!',
          3000
        );
      },
      errors => {
        this.deleteIndicator = false;
        if (errors.errors) {
          if (errors.errors.error) {
            this.uiService.showSnackBar(
              errors.error.error,
              3000
            );
          } else {
            this.uiService.showSnackBar(
              'Error occured! Unable to delete unpaid storage license at the moment.',
              3000
            );
          }
        } else {
          this.uiService.showSnackBar(
            'Error occured! Unable to delete unpaid storage license at the moment.',
            3000
          );
        }
      }
    );
  }

  retryPayment(lic, productIndex: number) {
    if (productIndex === 0) {
      this.router.navigate([ window.location.pathname + '/retry-common-license-payment/' + lic.order_pk]);
    } else if (productIndex === 1) {
      this.router.navigate([ window.location.pathname + '/retry-storage-license-payment/' + lic.order_pk]);
    }
  }

  purchaseLicense() {
    this.router.navigate([window.location.pathname + '/choose-product-type']);
  }
}
