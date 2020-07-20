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

  constructor( private media: MediaMatcher ) {
    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    localStorage.setItem('activeRoute', 'LICENSE');
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

}
