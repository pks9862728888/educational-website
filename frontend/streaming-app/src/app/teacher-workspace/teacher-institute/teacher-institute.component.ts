import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { InAppDataTransferService } from '../../in-app-data-transfer.service';
import { COUNTRY, STATE, INSTITUTE_CATEGORY, INSTITUTE_ROLE, INSTITUTE_TYPE_REVERSE, INSTITUTE_ROLE_REVERSE } from './../../../constants';
import { InstituteApiService } from '../../services/institute-api.service';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, OnDestroy, Inject } from '@angular/core';
import { MAT_SNACK_BAR_DATA, MatSnackBar } from '@angular/material/snack-bar';
import { ApiService } from '../../services/api.service';

interface TeacherInstitutesMinDetailInterface {
  id: number;
  name: string;
  country: string;
  institute_category: string;
  type: string;
  created_date: string;
  institute_slug: string;
  role: string;
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
    no_of_admin: number;
  };
}


interface InstituteCreatedEvent {
  status: boolean;
  url: string;
  type: string;
}


interface StatusResponse {
  status: string;
}


interface NameExistsStatus {
  status: boolean;
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
  templateUrl: './teacher-institute.component.html',
  styleUrls: ['./teacher-institute.component.css']
})
export class TeacherInstituteComponent implements OnInit, OnDestroy {

  mobileQuery: MediaQueryList;

  // For handling filters
  appliedFilter = 'NONE';

  // For handling search results
  searched = false;

  // For handling views
  showInstituteListView = true;
  showCreateInstituteProgressSpinner: boolean;
  showJoinInstituteProgressSpinner: boolean;
  createInstituteDisabled: boolean;

  // For handling expansion panel
  searchedInstituteStep: number;
  adminInstituteStep: number;
  joinedInstituteStep: number;
  pendingInstituteInviteStep: number;

  // For handling star rating
  rating = 4;

  // For storing admin institutes
  teacherAdminInstitutesMinList: TeacherInstitutesMinDetailInterface[] = [];
  teacherJoinedInstituteMinList:TeacherInstitutesMinDetailInterface[] = [];
  pendingInstituteInviteMinList: TeacherInstitutesMinDetailInterface[] = [];

  // For handling views based on input from breadcrumb
  showInstituteListViewSubscription: Subscription;

  // For handling institute preview view
  currentSelectedInstituteUrl: string;

  // For showing status results
  instituteJoinDeclineError: string;
  createInstituteError: string;

  constructor(private media: MediaMatcher,
              private instituteApiService: InstituteApiService,
              private apiService: ApiService,
              private inAppDataTransferService: InAppDataTransferService,
              private snackBar: MatSnackBar,
              private router: Router ) {
    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    // this.router.navigate(['teacher-workspace/institutes/' + 'tempView' + '/permissions']);
    sessionStorage.setItem('activeRoute', 'INSTITUTES');
    this.instituteApiService.getTeacherAdminInstituteMinDetails().subscribe(
      (result: TeacherInstitutesMinDetailInterface[]) => {
        for (const institute of result) {
          this.teacherAdminInstitutesMinList.push(institute);
        }
      },
      error => {}
    );

    this.instituteApiService.getJoinedInstituteMinDetails().subscribe(
      (result: TeacherInstitutesMinDetailInterface[]) => {
        for (const institute of result) {
          this.teacherJoinedInstituteMinList.push(institute);
        }
      },
      error => {}
    );

    this.instituteApiService.getInvitedInstituteMinDetails().subscribe(
      (result: TeacherInstitutesMinDetailInterface[]) => {
        for (const institute of result) {
          this.pendingInstituteInviteMinList.push(institute);
        }
      },
      error => {}
    );

    // Subscribing to show the list view on input from breadcrumb
    this.showInstituteListViewSubscription = this.inAppDataTransferService.setInstituteViewActive$.subscribe(
      (status: boolean) => {
        this.showInstituteListView = status;
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

  setPendingInstituteInviteStep(index: number) {
    this.pendingInstituteInviteStep = index;
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

  // Returns true if empty, else false
  isMyInstituteEmpty() {
    return this.teacherAdminInstitutesMinList.length === 0;
  }

  isJoinedInstituteEmpty() {
    return this.teacherJoinedInstituteMinList.length === 0;
  }

  isPendingInstituteEmpty() {
    return this.pendingInstituteInviteMinList.length === 0;
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
    this.showCreateInstituteProgressSpinner = true;
    this.createInstituteError = null;
    this.apiService.checkNameExists().subscribe(
      (result: NameExistsStatus) => {
        if (result.status === true) {
          this.showCreateInstituteProgressSpinner = false;
          this.showInstituteListView = false;
          this.inAppDataTransferService.sendActiveBreadcrumbLinkData('CREATE');
        } else {
          this.showCreateInstituteProgressSpinner = false;
          this.createInstituteDisabled = true;
          this.createInstituteError = 'First fill out your profile details & then try again.';
        }
      },
      error => {}
    )
  }

  previewClicked(instituteSlug: string, role:string, type: string) {
    sessionStorage.setItem('currentInstituteSlug', instituteSlug);
    sessionStorage.setItem('currentInstituteRole', role);
    sessionStorage.setItem('currentInstituteType', type);

    if (type === INSTITUTE_TYPE_REVERSE.School) {
      sessionStorage.setItem('activeRoute', 'SCHOOL_PROFILE');
      this.router.navigate(['school-workspace/' + instituteSlug + '/profile']);
    } else if (type === INSTITUTE_TYPE_REVERSE.College) {
      sessionStorage.setItem('activeRoute', 'COLLEGE_PROFILE');
      this.router.navigate(['college-workspace/' + instituteSlug + '/profile']);
    } else {
      sessionStorage.setItem('activeRoute', 'COACHING_PROFILE');
      this.router.navigate(['coaching-workspace/' + instituteSlug + '/profile']);
    }
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

      // Routing to institute preview
      const instituteSlug = event.url.substring(event.url.lastIndexOf('/') + 1, event.url.length);
      sessionStorage.setItem('currentInstituteSlug', instituteSlug);
      sessionStorage.setItem('currentInstituteType', event.type);
      sessionStorage.setItem('currentInstituteRole', INSTITUTE_ROLE_REVERSE['Admin']);

      if (event.type === INSTITUTE_TYPE_REVERSE['School']) {
        sessionStorage.setItem('activeRoute', 'SCHOOL_PROFILE');
        this.router.navigate(['school-workspace/' + instituteSlug + '/profile']);
      } else if (event.type === INSTITUTE_TYPE_REVERSE['College']) {
        sessionStorage.setItem('activeRoute', 'COLLEGE_PROFILE');
        this.router.navigate(['college-workspace/' + instituteSlug + '/profile']);
      } else {
        sessionStorage.setItem('activeRoute', 'COACHING_PROFILE');
        this.router.navigate(['coaching-workspace/' + instituteSlug + '/profile']);
      }
    } else {
      this.showInstituteListView = true;
      this.inAppDataTransferService.sendActiveBreadcrumbLinkData('');
    }
  }

  joinInstitute(institute: TeacherInstitutesMinDetailInterface) {
    this.showJoinInstituteProgressSpinner = true;
    this.instituteJoinDeclineError = null;
    this.apiService.checkNameExists().subscribe(
      (result: NameExistsStatus) => {
        if (result.status === true) {
          this.showJoinInstituteProgressSpinner = false;
          this.instituteApiService.acceptDeleteInstituteJoinInvitation(
            institute.institute_slug, 'ACCEPT').subscribe(
            (result: StatusResponse) => {
              if (result.status === 'ACCEPTED') {
                this.teacherJoinedInstituteMinList.push(institute);
                this.pendingInstituteInviteMinList.splice(this.pendingInstituteInviteMinList.indexOf(institute));
                // Show snackbar
                this.snackBar.openFromComponent(SnackbarComponent, {
                  data: 'Institute joined successfully!',
                  duration: 2000
                });
              }
            },
            error => {
              if (error.error) {
                if (error.error.error) {
                  this.instituteJoinDeclineError = error.error.error;
                }
              } else {
                this.instituteJoinDeclineError = 'Unable to process request. Refresh and try again.';
              }
            }
          )
        } else {
            this.showJoinInstituteProgressSpinner = false;
            this.instituteJoinDeclineError = 'Error! First fill out your profile details.';
        }
      },
      error => {
        this.instituteJoinDeclineError = 'Unable to process request. Refresh and try again.';
      }
    );


  }

  declineInvitation(institute: TeacherInstitutesMinDetailInterface) {
    this.instituteJoinDeclineError = null;
    this.instituteApiService.acceptDeleteInstituteJoinInvitation(institute.institute_slug, 'DELETE').subscribe(
      (result: StatusResponse) => {
        if (result.status === 'DELETED') {
          this.pendingInstituteInviteMinList.splice(this.pendingInstituteInviteMinList.indexOf(institute), 1);
          // Show snackbar
          this.snackBar.openFromComponent(SnackbarComponent, {
            data: 'Institute join request declined!',
            duration: 2000
          });
        }
      },
      error => {
        if (error.error) {
          if (error.error.error) {
            this.instituteJoinDeclineError = error.error.error;
          } else {
            this.instituteJoinDeclineError = 'Unable to process request. Refresh and try again.';
          }
        }
      }
    )
  }

  getRole(key: string) {
    return INSTITUTE_ROLE[key];
  }

  ngOnDestroy() {
    if (this.showInstituteListViewSubscription) {
      this.showInstituteListViewSubscription.unsubscribe();
    }
  }
}
