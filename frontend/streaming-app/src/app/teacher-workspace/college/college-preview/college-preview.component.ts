import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, ParamMap, Router } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { InAppDataTransferService } from 'src/app/in-app-data-transfer.service';
import { InstituteApiService } from 'src/app/institute-api.service';
import { INSTITUTE_CATEGORY, COUNTRY, STATE, LANGUAGE } from 'src/constants';

interface InstituteDetails {
  user: string;
  name: string;
  country: string;
  institute_category: string;
  institute_slug: string;
  created_date: string;
  institute_profile: {
    motto: string;
    email: string;
    phone: string;
    website_url: string;
    state: string;
    pin: string;
    address: string;
    recognition: string;
    primary_language: string;
    secondary_language: string;
    tertiary_language: string;
  };
  institute_logo: {
    image: string;
  };
  institute_banner: {
    image: string;
  }
}


@Component({
  selector: 'app-college-preview',
  templateUrl: './college-preview.component.html',
  styleUrls: ['./college-preview.component.css']
})
export class CollegePreviewComponent implements OnInit {

  mobileQuery: MediaQueryList;

  // To store current institute details
  currentInstituteSlug: string;
  currentInstituteDetails: InstituteDetails;

  // Delete it
  bannerPresent = false;

  constructor( private router: Router,
               private route: ActivatedRoute,
               private media: MediaMatcher,
               private inAppDataTransferService: InAppDataTransferService,
               private instituteApiService: InstituteApiService ) {
                this.mobileQuery = this.media.matchMedia('(max-width: 600px)');
                this.inAppDataTransferService.showInstituteSidenavView(true);
               }

  ngOnInit(): void {
    this.route.paramMap
      .subscribe((params: ParamMap) => {
        this.currentInstituteSlug = params.get('name');
      });

    this.instituteApiService.getInstituteDetails(this.currentInstituteSlug).subscribe(
      (result: InstituteDetails) => {
        this.currentInstituteDetails = result;
      }
    )
  }

  // To navigate back to my institutes preview
  backClicked() {
    this.inAppDataTransferService.showInstituteSidenavView(false);
    this.inAppDataTransferService.sendActiveBreadcrumbLinkData('');
    this.router.navigate(['teacher-workspace/institutes']);
  }

  // To get the name from the key
  getInstituteType(key: string) {
    return INSTITUTE_CATEGORY[key];
  }

  getInstituteCountry(key: string) {
    return COUNTRY[key];
  }

  getState(key: string) {
    return STATE[key];
  }

  getEmailLink(email: string) {
    return "mailto:" + email;
  }

  getLanguage(key: string) {
    return LANGUAGE[key];
  }

  getRole() {
    const userId = sessionStorage.getItem('user_id')
    if (this.currentInstituteDetails.user.toString() === userId) {
      return 'Admin';
    }
  }

}
