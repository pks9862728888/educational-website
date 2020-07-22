import { INSTITUTE_LICENSE_PLANS, DISCUSSION_FORUM_PER_ATTENDEES } from './../../constants';
import { InstituteApiService } from 'src/app/institute-api.service';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';


interface LicenseList {
  'id': number;
  'billing': string;
  'type': string;
  'cost': number;
  'discount': number;
  'storage': number;
  'no_of_admin': number;
  'no_of_staff': number;
  'no_of_faculty': number;
  'no_of_student': number;
  'video_call_max_attendees': number;
  'classroom_limit': number;
  'department_limit': number;
  'subject_limit': number;
  'scheduled_test': boolean;
  'discussion_forum': string;
  'LMS_exists': boolean
}

interface InstituteLicenseInterface {
  'monthly_license': LicenseList[]
  'yearly_license': LicenseList[]
}

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

  monthlyLicensePlans: LicenseList[];
  yearlyLicensePlans: LicenseList[];

  constructor( private media: MediaMatcher,
               private instituteApiService: InstituteApiService ) {
    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    sessionStorage.setItem('activeRoute', 'LICENSE');
    this.instituteApiService.getInstituteLicenseList().subscribe(
      (result: InstituteLicenseInterface) => {
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

  calculateCostInThousands(cost:number, discount: number) {
    return (cost * (1 - discount/100))/1000;
  }

}
