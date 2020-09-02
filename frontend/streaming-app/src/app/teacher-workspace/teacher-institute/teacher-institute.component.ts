import { UiService } from './../../services/ui.service';
import { TeacherInstitutesMinDetailInterface, NameExistsStatus, InstituteCreatedEvent, StatusResponse } from './../../models/institute.model';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { InAppDataTransferService } from '../../services/in-app-data-transfer.service';
import { COUNTRY,
         STATE,
         INSTITUTE_CATEGORY,
         INSTITUTE_ROLE,
         INSTITUTE_TYPE_REVERSE,
         INSTITUTE_ROLE_REVERSE,
         currentInstituteRole,
         currentInstituteSlug,
         currentInstituteType } from './../../../constants';
import { InstituteApiService } from '../../services/institute-api.service';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ApiService } from '../../services/api.service';


@Component({
  selector: 'app-teacher-college',
  templateUrl: './teacher-institute.component.html',
  styleUrls: ['./teacher-institute.component.css']
})
export class TeacherInstituteComponent implements OnInit, OnDestroy {

  mq: MediaQueryList;

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
  currentSelectedInstituteUrl: string;
  instituteJoinDeclineError: string;
  createInstituteError: string;

  constructor(
    private media: MediaMatcher,
    private instituteApiService: InstituteApiService,
    private apiService: ApiService,
    private uiService: UiService,
    private inAppDataTransferService: InAppDataTransferService,
    private snackBar: MatSnackBar,
    private router: Router ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
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
          this.createInstituteError = 'Error! First fill out your profile details & then try again.';
        }
      },
      error => {}
    );
  }

  previewClicked(instituteSlug: string, role:string, type: string) {
    sessionStorage.setItem(currentInstituteSlug, instituteSlug);
    sessionStorage.setItem(currentInstituteRole, role);
    sessionStorage.setItem(currentInstituteType, type);
    this.navigateToProfile(type, instituteSlug);
  }

  // Taking action based on whether institute is created or not
  instituteCreated(event: InstituteCreatedEvent){
    if (event.status === true) {
      this.currentSelectedInstituteUrl = event.url;
      this.uiService.showSnackBar(
        'Institute created successfully!',
        2000
      );
      // Routing to institute preview
      const instituteSlug = event.url.substring(event.url.lastIndexOf('/') + 1, event.url.length);
      sessionStorage.setItem('currentInstituteSlug', instituteSlug);
      sessionStorage.setItem('currentInstituteType', event.type);
      sessionStorage.setItem('currentInstituteRole', INSTITUTE_ROLE_REVERSE['Admin']);

      this.navigateToProfile(event.type, instituteSlug);
    } else {
      this.showInstituteListView = true;
      this.inAppDataTransferService.sendActiveBreadcrumbLinkData('');
    }
  }

  navigateToProfile(type: string, instituteSlug: string) {
    if (type === INSTITUTE_TYPE_REVERSE['School']) {
      this.router.navigate(['school-workspace/' + instituteSlug + '/profile']);
    } else if (type === INSTITUTE_TYPE_REVERSE['College']) {
      this.router.navigate(['college-workspace/' + instituteSlug + '/profile']);
    } else {
      this.router.navigate(['coaching-workspace/' + instituteSlug + '/profile']);
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
                this.uiService.showSnackBar(
                  'Institute joined successfully!', 2000
                );
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
          this.uiService.showSnackBar(
            'Institute join request declined!',  2000
          );
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

  closeJoinDeclineError() {
    this.instituteJoinDeclineError = null;
  }

  closeCreateInstituteError() {
    this.createInstituteError = null;
  }

  ngOnDestroy() {
    if (this.showInstituteListViewSubscription) {
      this.showInstituteListViewSubscription.unsubscribe();
    }
  }
}
