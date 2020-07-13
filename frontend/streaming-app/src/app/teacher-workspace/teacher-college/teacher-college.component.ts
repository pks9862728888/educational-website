import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { InAppDataTransferService } from '../../in-app-data-transfer.service';
import { COUNTRY, STATE, INSTITUTE_CATEGORY } from './../../../constants';
import { InstituteApiService } from './../../institute-api.service';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, OnDestroy, Inject } from '@angular/core';
import { MAT_SNACK_BAR_DATA, MatSnackBar } from '@angular/material/snack-bar';

interface TeacherAdminInstitutesMin {
  id: number;
  user: number;
  name: string;
  country: string;
  institute_category: string;
  created_date: string;
  institute_slug: string;
  institute_profile: {
    motto: string;
    email: string;
    phone: string;
    website_url: string;
    state: string;
    recognition: string;
  };
  institute_logo: {
    image: string;
  };
  institute_statistics: {
    no_of_students: number;
    no_of_faculties: number;
    no_of_staff: number;
  };
}


interface InstituteCreatedEvent {
  status: boolean;
  url: string;
}


// For showing snackbar
@Component({
  template: `
    <div class="snackbar-text">
      {{ this.message }}
    </div>
  `,
  styles: [`
    .snackbar-text {
      color: yellow;
      text-align: center;
    }
  `]
})
export class SnackbarComponent {
  constructor(@Inject(MAT_SNACK_BAR_DATA) public message: string) { }
}


@Component({
  selector: 'app-teacher-college',
  templateUrl: './teacher-college.component.html',
  styleUrls: ['./teacher-college.component.css']
})
export class TeacherCollegeComponent implements OnInit, OnDestroy {

  mobileQuery: MediaQueryList;

  // For handling filters
  appliedFilter = 'NONE';

  // For handling search results
  searched = false;

  // For handling views
  createInstituteClicked = false;

  // For handling expansion panel
  searchedInstituteStep: number;
  adminInstituteStep: number;
  joinedInstituteStep: number;

  // For handling star rating
  rating = 4;

  // For storing admin institutes
  teacherAdminInstitutesMinList: TeacherAdminInstitutesMin[] = [];

  // For handling views based on input from breadcrumb
  showInstituteListViewSubscription: Subscription;

  // For handling institute preview view
  currentSelectedInstituteUrl: string;

  constructor(private media: MediaMatcher,
              private instituteApiService: InstituteApiService,
              private inAppDataTransferService: InAppDataTransferService,
              private snackBar: MatSnackBar,
              private router: Router ) {
    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    // this.router.navigate(['teacher-workspace/institutes/' + 'tempView' + '/permissions']);
    this.instituteApiService.getTeacherAdminInstituteMinDetails().subscribe(
      (result: TeacherAdminInstitutesMin[]) => {
        console.log(result);
        for (const institute of result) {
          this.teacherAdminInstitutesMinList.push(institute);
        }
      },
      error => {
        console.error(error);
      }
    );

    // Subscribing to show the list view on input from breadcrumb
    this.showInstituteListViewSubscription = this.inAppDataTransferService.setInstituteViewActive$.subscribe(
      (status: boolean) => {
        this.createInstituteClicked = false;
      }
    );
  }

  // For controlling expansion panel functioning
  setAdminInstituteStep(index: number) {
    this.adminInstituteStep = index;
  }

  setJoinedInstituteStep(index: number) {
    this.joinedInstituteStep = index;
  }

  setSearchedInstituteStep(index: number) {
    this.searchedInstituteStep = index;
  }

  // For checking filter
  checkFilter(filterName: string) {
    if (this.appliedFilter === filterName) {
      return true;
    } else {
      return false;
    }
  }

  applyFilter(filterName: string) {
    this.appliedFilter = filterName;
  }

  // Returns true if my institute list is empty, else false
  isMyInstituteEmpty() {
    return this.teacherAdminInstitutesMinList.length === 0;
  }

  // Decoding the respective keys
  decodeCountry(key: string) {
    return COUNTRY[key];
  }

  decodeState(key: string) {
    return STATE[key];
  }

  decodeCategory(key: string) {
    return INSTITUTE_CATEGORY[key];
  }

  createInstitute() {
    this.createInstituteClicked = true;
    this.inAppDataTransferService.sendActiveBreadcrumbLinkData('CREATE');
  }

  previewClicked(instituteSlug: string) {
    // Showing appropriate navigation in breadcrumb
    this.inAppDataTransferService.sendActiveBreadcrumbLinkData('INSTITUTE_PROFILE');
    localStorage.setItem('currentInstituteSlug', instituteSlug);
    this.router.navigate(['teacher-workspace/institutes/preview/', instituteSlug]);
  }

  // Taking action based on whether institute is created or not
  instituteCreated(event: InstituteCreatedEvent){
    if (event.status === true) {
      // Saving the url and showing appropriate message
      this.currentSelectedInstituteUrl = event.url;

      // Show snackbar
      this.snackBar.openFromComponent(SnackbarComponent, {
        data: 'Institute created successfully!',
        duration: 2000
      });

      // Showing appropriate navigation in breadcrumb
      this.inAppDataTransferService.sendActiveBreadcrumbLinkData('PREVIEW');

      // Routing to institute preview
      const instituteSlug = event.url.substring(event.url.lastIndexOf('/') + 1, event.url.length);
      localStorage.setItem('currentInstituteSlug', instituteSlug);
      this.router.navigate(['teacher-workspace/institutes/preview', instituteSlug]);
    } else {
      this.createInstituteClicked = false;
      this.inAppDataTransferService.sendActiveBreadcrumbLinkData('');
    }
  }

  ngOnDestroy() {
    this.showInstituteListViewSubscription.unsubscribe();
  }
}
