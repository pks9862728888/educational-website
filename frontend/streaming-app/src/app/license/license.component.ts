import { Subscription } from 'rxjs';
import { InAppDataTransferService } from './../services/in-app-data-transfer.service';
import { INSTITUTE_LICENSE_PLANS, BILLING_TERM, UNLIMITED, DISCUSSION_FORUM_PER_ATTENDEES, INSTITUTE_TYPE_REVERSE, purchasedLicenseExists } from './../../constants';
import { Router } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { InstituteApiService } from '../services/institute-api.service';
import { PaidLicenseResponse, ActiveLicenseDetails, PurchasedInactiveLicenseDetails, ExpiredLicenseDetails } from './license.model';


@Component({
  selector: 'app-license',
  templateUrl: './license.component.html',
  styleUrls: ['./license.component.css']
})
export class LicenseComponent implements OnInit, OnDestroy {

  mobileQuery: MediaQueryList;
  fetchedLicenseDetails: boolean;
  fetchActiveLicenseIndicator: boolean;
  reloadErrorText: string;
  errorText: string;
  currentInstituteSlug: string;
  activeLicenseDetails: ActiveLicenseDetails;
  expiredLicenseDetails: ExpiredLicenseDetails;
  purchasedInactiveLicenseDetails: PurchasedInactiveLicenseDetails;
  UNLIMITED = UNLIMITED;

  // For controlling expansion panel
  licenseStep: number;
  canPurchaseAnotherLicense: boolean;

  constructor( private media: MediaMatcher,
               private router: Router,
               private instituteApiService: InstituteApiService,
               private inAppDataTransferService: InAppDataTransferService) {
    this.mobileQuery = this.media.matchMedia('(max-width: 540px)');
    this.currentInstituteSlug = sessionStorage.getItem('currentInstituteSlug');
    this.fetchedLicenseDetails = false;
    this.canPurchaseAnotherLicense = true;
  }

  ngOnInit() {
    this.fetchLicenseDetails();
  }

  fetchLicenseDetails() {
    this.fetchActiveLicenseIndicator = true;
    this.reloadErrorText = null;
    this.instituteApiService.getInstituteLicensePurchased(this.currentInstituteSlug).subscribe(
      (result: PaidLicenseResponse) => {
        this.activeLicenseDetails = result.active_license;
        this.purchasedInactiveLicenseDetails = result.purchased_inactive_license;
        this.expiredLicenseDetails = result.expired_license;
        this.fetchedLicenseDetails = true;
        this.fetchActiveLicenseIndicator = false;
        this.purchasedInactiveLicenseExists();
      },
      errors => {
        this.fetchActiveLicenseIndicator = false;
        if (errors.error) {
          if(errors.error.error) {
            this.errorText = errors.error.error;
          } else {
            this.reloadErrorText = 'Unable to fetch licence details.';
          }
        } else {
          this.reloadErrorText = 'Unable to fetch licence details.';
        }
      }
    );
  }

  setLicenseStep(step: number) {
    this.licenseStep = step;
  }

  retryClicked() {
    this.fetchLicenseDetails();
  }

  closeErrorTextClicked() {
    this.errorText = null;
  }

  activeLicenseExists() {
    const status =  Object.keys(this.activeLicenseDetails).length !== 0;
    if (status) {
      this.inAppDataTransferService.showTeacherFullInstituteView();
    } else {
      sessionStorage.setItem(purchasedLicenseExists, 'false');
    }
    return status;
  }

  expiredLicenseExists() {
    return Object.keys(this.expiredLicenseDetails).length !== 0;
  }

  purchasedInactiveLicenseExists() {
    const status =  Object.keys(this.purchasedInactiveLicenseDetails).length !== 0;
    if (status) {
      sessionStorage.setItem(purchasedLicenseExists, 'true');
      this.inAppDataTransferService.showTeacherFullInstituteView();
      this.canPurchaseAnotherLicense = false;
    } else {
      sessionStorage.setItem(purchasedLicenseExists, 'false');
    }
    return status;
}

  getLicensePlan(key: string) {
    return INSTITUTE_LICENSE_PLANS[key];
  }

  getBillingType(key: string) {
    return BILLING_TERM[key];
  }

  getDiscussionForum(key: string) {
    return DISCUSSION_FORUM_PER_ATTENDEES[key];
  }

  purchaseLicense() {
    if (sessionStorage.getItem('currentInstituteType') === INSTITUTE_TYPE_REVERSE['School']) {
      this.router.navigate(['/school-workspace/' + this.currentInstituteSlug + '/license/purchase']);
    } else if (sessionStorage.getItem('currentInstituteType') === INSTITUTE_TYPE_REVERSE['College']) {
      this.router.navigate(['/college-workspace/' + this.currentInstituteSlug + '/license/purchase']);
    } else if (sessionStorage.getItem('currentInstituteType') === INSTITUTE_TYPE_REVERSE['Coaching']) {
      this.router.navigate(['/coaching-workspace/' + this.currentInstituteSlug + '/license/purchase']);
    }
  }

  ngOnDestroy() {}
}
