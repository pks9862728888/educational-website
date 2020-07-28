import { Router } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-license',
  templateUrl: './license.component.html',
  styleUrls: ['./license.component.css']
})
export class LicenseComponent implements OnInit {

  mobileQuery: MediaQueryList;
  fetchActiveLicenseIndicator: boolean;
  reloadErrorText: string;

  // For controlling expansion panel
  licenseStep: number;

  constructor( private media: MediaMatcher,
               private router: Router ) {
    this.mobileQuery = this.media.matchMedia('(max-width: 540px)');
  }

  ngOnInit() {
    sessionStorage.setItem('activeRoute', 'LICENSE');
  }

  setLicenseStep(step: number) {
    this.licenseStep = step;
  }

  retryClicked() {
    // Retry reloading
  }
}
