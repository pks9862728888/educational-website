import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { InAppDataTransferService } from '../../services/in-app-data-transfer.service';
import { InstituteApiService } from '../../services/institute-api.service';
import { INSTITUTE_CATEGORY, COUNTRY, STATE, LANGUAGE, INSTITUTE_ROLE } from 'src/constants';

interface InstituteDetails {
  user: string;
  name: string;
  country: string;
  institute_category: string;
  institute_slug: string;
  created_date: string;
  role: string;
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
  institute_statistics: {
    no_of_admin: number;
    no_of_students: number;
    no_of_faculties: number;
    no_of_staff: number;
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
  templateUrl: './college-profile.component.html',
  styleUrls: ['./college-profile.component.css']
})
export class CollegeProfileComponent implements OnInit {

  mobileQuery: MediaQueryList;

  // To store current institute details
  currentInstituteSlug: string;
  currentInstituteRole: string;
  currentInstituteDetails: InstituteDetails;

  // Delete it
  bannerPresent = false;

  constructor( private router: Router,
               private media: MediaMatcher,
               private inAppDataTransferService: InAppDataTransferService,
               private instituteApiService: InstituteApiService ) {
    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.currentInstituteSlug = sessionStorage.getItem('currentInstituteSlug');
    this.currentInstituteRole = sessionStorage.getItem('currentInstituteRole');
    this.instituteApiService.getInstituteDetails(this.currentInstituteSlug).subscribe(
      (result: InstituteDetails) => {
        this.currentInstituteDetails = result;
      }
    )
  }

  // To navigate back to my institutes preview
  exitClicked() {
    this.inAppDataTransferService.sendActiveBreadcrumbLinkData('');
    sessionStorage.removeItem('currentInstituteSlug');
    sessionStorage.removeItem('currentInstituteRole');
    sessionStorage.setItem('activeRoute', 'INSTITUTES');
    this.router.navigate(['/teacher-workspace/institutes']);
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
    return INSTITUTE_ROLE[this.currentInstituteDetails.role]
  }

}
