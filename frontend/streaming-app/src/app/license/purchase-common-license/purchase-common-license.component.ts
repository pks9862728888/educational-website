import { Component, OnInit } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';
import { InstituteApiService } from '../../services/institute-api.service';
import { Router } from '@angular/router';
import { InstituteLicenseList, LicenseDetails } from '../../models/license.model';
import { INSTITUTE_TYPE_REVERSE,
         BILLING_TERM,
         INSTITUTE_LICENSE_PLANS,
         UNLIMITED, currentInstituteSlug } from 'src/constants';
import { MatDialog } from '@angular/material/dialog';
import { UiDialogComponent } from 'src/app/shared/ui-dialog/ui-dialog.component';
import { UiService } from 'src/app/services/ui.service';
import { getDateFromUnixTimeStamp } from 'src/app/format-datepicker';

@Component({
  selector: 'app-purchase-common-license',
  templateUrl: './purchase-common-license.component.html',
  styleUrls: ['./purchase-common-license.component.css']
})
export class PurchaseCommonLicenseComponent implements OnInit {

  mq: MediaQueryList;
  showLoadingIndicator: boolean;
  loadingText = 'Loading Institute Common License Plans...';
  loadingErrorText: string;
  showReload: boolean;
  UNLIMITED = UNLIMITED;

  // For controlling billing term
  activeBilling = 'MONTHLY';
  activePlanContainer = 'BUSINESS';

  monthlyLicensePlans: LicenseDetails[];
  yearlyLicensePlans: LicenseDetails[];
  currentActiveLicensePlans: LicenseDetails[];

  constructor(
    private media: MediaMatcher,
    private instituteApiService: InstituteApiService,
    private router: Router
    ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.getInstituteLicenseList();
  }

  getInstituteLicenseList() {
    this.showLoadingIndicator = true;
    this.loadingErrorText = null;
    this.showReload = false;
    const instituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.instituteApiService.getInstituteLicenseList(
      instituteSlug
    ).subscribe(
      (result: InstituteLicenseList) => {
        this.showLoadingIndicator = false;
        this.monthlyLicensePlans = result.monthly_license;
        this.yearlyLicensePlans = result.yearly_license;
        this.currentActiveLicensePlans = this.monthlyLicensePlans;
      },
      errors => {
        this.showLoadingIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.loadingErrorText = errors.error.error;
          } else {
            this.showReload = true;
          }
        } else {
          this.showReload = true;
        }
      }
    );
  }

  reloadLicensePlans() {
    this.getInstituteLicenseList();
  }

  changeBillingTerm(term: string) {
    if (!(this.activeBilling === term)) {
      this.activeBilling = term;
      if (this.activeBilling === 'YEARLY') {
        this.currentActiveLicensePlans = this.yearlyLicensePlans;
      } else {
        this.currentActiveLicensePlans = this.monthlyLicensePlans;
      }
    }
  }

  changeActivePlanContainer(plan: string) {
    if (!(this.activePlanContainer === plan)) {
      this.activePlanContainer = plan;
    }
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
    if (sessionStorage.getItem('currentInstituteType') === INSTITUTE_TYPE_REVERSE.College) {
      return true;
    } else {
      return false;
    }
  }

  selectedLicense(id: string) {
    sessionStorage.setItem('selectedLicenseId', id);
    this.router.navigate(
      ['/school-workspace/' + sessionStorage.getItem('currentInstituteSlug') + '/license/review']);
  }

  isDiscountPresent(discount: number) {
    if (Math.abs(discount)) {
      return true;
    } else {
      return false;
    }
  }

  navigateToChooseProductType() {
    const urlLocation = window.location.pathname;
    const loc  = urlLocation.slice(0, urlLocation.length - '/purchase-common-license'.length);
    this.router.navigate([ loc + '/choose-product-type']);
  }
}
