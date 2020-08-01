import { Component, OnInit } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';
import { InstituteApiService } from '../../services/institute-api.service';
import { Router } from '@angular/router';
import { InstituteLicenseList, LicenseDetails } from '../license.model';
import { INSTITUTE_TYPE_REVERSE, DISCUSSION_FORUM_PER_ATTENDEES, BILLING_TERM, INSTITUTE_LICENSE_PLANS } from 'src/constants';

@Component({
  selector: 'app-purchase-license',
  templateUrl: './purchase-license.component.html',
  styleUrls: ['./purchase-license.component.css']
})
export class PurchaseLicenseComponent implements OnInit {

  mobileQuery: MediaQueryList;

  // For controlling billing term
  activeBilling = 'MONTHLY';
  activePlanContainer = 'BUSINESS';

  monthlyLicensePlans: LicenseDetails[];
  yearlyLicensePlans: LicenseDetails[];
  currentActiveLicensePlans: LicenseDetails[];

  constructor( private media: MediaMatcher,
               private instituteApiService: InstituteApiService,
               private router: Router ) {
    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.instituteApiService.getInstituteLicenseList().subscribe(
      (result: InstituteLicenseList) => {
        this.monthlyLicensePlans = result.monthly_license;
        this.yearlyLicensePlans = result.yearly_license;
        this.currentActiveLicensePlans = this.monthlyLicensePlans;
      }
    );
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

  getDiscussionForums(key: string) {
    return DISCUSSION_FORUM_PER_ATTENDEES[key];
  }

  calculateCostInThousands(amount:number, discountPercent: number) {
    return (amount * (1 - discountPercent/100))/1000;
  }

  instituteIsCoaching() {
    if (sessionStorage.getItem('currentInstituteType') === INSTITUTE_TYPE_REVERSE['Coaching']) {
      return true
    } else {
      return false
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
}
