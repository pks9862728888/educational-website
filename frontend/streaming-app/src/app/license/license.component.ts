import { Router } from '@angular/router';
import { LicenseDetails, InstituteLicenseList } from './license.model';
import { INSTITUTE_LICENSE_PLANS, DISCUSSION_FORUM_PER_ATTENDEES, INSTITUTE_TYPE_REVERSE } from './../../constants';
import { InstituteApiService } from 'src/app/institute-api.service';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-license',
  templateUrl: './license.component.html',
  styleUrls: ['./license.component.css']
})
export class LicenseComponent implements OnInit {

  mobileQuery: MediaQueryList;

  // For controlling billing term
  activeBilling = 'MONTHLY';
  activePlanContainer = 'BUSINESS';

  monthlyLicensePlans: LicenseDetails[];
  yearlyLicensePlans: LicenseDetails[];

  constructor( private media: MediaMatcher,
               private instituteApiService: InstituteApiService,
               private router: Router ) {
    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    sessionStorage.setItem('activeRoute', 'LICENSE');
    this.instituteApiService.getInstituteLicenseList().subscribe(
      (result: InstituteLicenseList) => {
        this.monthlyLicensePlans = result.monthly_license;
        this.yearlyLicensePlans = result.yearly_license;
      }
    );
  }

  changeBillingTerm(term: string) {
    if (!(this.activeBilling === term)) {
      this.activeBilling = term;
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
      ['/school-workspace/' + sessionStorage.getItem('currentInstituteSlug') + '/license/review'])
  }
}
