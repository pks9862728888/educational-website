import { Router } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { InstituteApiService } from '../services/institute-api.service';


@Component({
  selector: 'app-license',
  templateUrl: './license.component.html',
  styleUrls: ['./license.component.css']
})
export class LicenseComponent implements OnInit {

  mobileQuery: MediaQueryList;
  fetchActiveLicenseIndicator: boolean;
  reloadErrorText: string;
  currentInstituteSlug: string;

  // For controlling expansion panel
  licenseStep: number;

  constructor( private media: MediaMatcher,
               private router: Router,
               private instituteApiService: InstituteApiService ) {
    this.mobileQuery = this.media.matchMedia('(max-width: 540px)');
    this.currentInstituteSlug = sessionStorage.getItem('currentInstituteSlug');
  }

  ngOnInit() {
    sessionStorage.setItem('activeRoute', 'LICENSE');
    this.fetchActiveLicenseIndicator = true;
    this.instituteApiService.getInstituteLicensePurchased(this.currentInstituteSlug).subscribe(
      (result) => {
        this.fetchActiveLicenseIndicator = false;
        console.log(result);

      },
      errors => {
        this.fetchActiveLicenseIndicator = false;
        console.log(errors);
      }
    )
  }

  setLicenseStep(step: number) {
    this.licenseStep = step;
  }

  retryClicked() {
    // Retry reloading
  }
}
