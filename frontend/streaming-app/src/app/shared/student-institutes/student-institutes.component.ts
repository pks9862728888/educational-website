import { Subscription } from 'rxjs';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { INSTITUTE_ROLE, COUNTRY, STATE, INSTITUTE_CATEGORY, currentInstituteRole, currentInstituteSlug, currentInstituteType, INSTITUTE_TYPE_REVERSE } from '../../../constants';
import { MediaMatcher } from '@angular/cdk/layout';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { ApiService } from 'src/app/services/api.service';
import { Router } from '@angular/router';
import { StatusResponse, TeacherInstitutesMinDetailInterface, StudentInstitutesMinDetailInterface, StudentGetInstitutesListInterface, UserProfileDetailsExistsStatus } from '../../models/institute.model';
import { UiService } from 'src/app/services/ui.service';


@Component({
  selector: 'app-student-institutes',
  templateUrl: './student-institutes.component.html',
  styleUrls: ['./student-institutes.component.css']
})
export class StudentInstitutesComponent implements OnInit, OnDestroy {

  mq: MediaQueryList;
  loadingIndicator: boolean;
  showJoinInstituteProgressSpinner: boolean;
  searchedInstituteStep: number;
  joinedInstituteStep: number;
  pendingInstituteInviteStep: number;
  rating = 4;
  currentSelectedInstituteUrl: string;
  instituteJoinDeclineError: string;
  showReload: boolean;
  deleteInvitationSubscription: Subscription;
  joinInstituteSubscription: Subscription;

  joinedInstitutes: StudentInstitutesMinDetailInterface[] = [];
  instituteInvites: StudentInstitutesMinDetailInterface[] = [];

  constructor(
    private media: MediaMatcher,
    private instituteApiService: InstituteApiService,
    private apiService: ApiService,
    private uiService: UiService,
    private router: Router ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.getMinInstituteDetails();
  }

  getMinInstituteDetails() {
    this.loadingIndicator = true;
    this.showReload = false;
    this.instituteApiService.getInstituteMinDetailsStudent().subscribe(
      (result: StudentGetInstitutesListInterface) => {
        this.joinedInstitutes = result.active_institutes;
        this.instituteInvites = result.invited_institutes;
        this.loadingIndicator = false;
      },
      error => {
        this.loadingIndicator = false;
        this.showReload = true;
      }
    );
  }

  setJoinedInstituteStep(index: number) {
    this.joinedInstituteStep = index;
  }

  setPendingInstituteInviteStep(index: number) {
    this.showJoinInstituteProgressSpinner = false;
    this.pendingInstituteInviteStep = index;
  }

  isJoinedInstituteEmpty() {
    return this.joinedInstitutes.length === 0;
  }

  isPendingInstituteEmpty() {
    return this.instituteInvites.length === 0;
  }

  previewClicked(instituteSlug: string, role:string, type: string) {
    sessionStorage.setItem(currentInstituteSlug, instituteSlug);
    sessionStorage.setItem(currentInstituteRole, role);
    sessionStorage.setItem(currentInstituteType, type);
    this.navigateToProfile(type, instituteSlug);
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

  getIndexOfInstitute(list: StudentInstitutesMinDetailInterface[], index: number) {
    for (let idx in list) {
      if (list[idx].id === index) {
        return parseInt(idx);
      }
    }
    return -1;
  }

  joinInstitute(institute: StudentInstitutesMinDetailInterface) {
    this.showJoinInstituteProgressSpinner = true;
    this.instituteJoinDeclineError = null;
    this.apiService.checkUserProfileDetailsExists().subscribe(
      (result: UserProfileDetailsExistsStatus) => {
        if (result.status === true) {
          this.joinInstituteSubscription = this.uiService.studentDetailsDialogData$.subscribe(
            data => {
              this.showJoinInstituteProgressSpinner = false;
              if (data === true) {
                this.instituteInvites.splice(
                  this.getIndexOfInstitute(this.instituteInvites, institute.id), 1
                );
                institute.institute_statistics.no_of_students += 1;
                this.joinedInstitutes.push(institute);
                this.uiService.showSnackBar(
                  'Institute joined successfully!', 2000
                );
              }
              this.joinInstituteSubscription.unsubscribe();
            }
          )
          this.uiService.openStudentDetailsConfirmDialog(institute.institute_slug);
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

  declineInvitationConfirm(institute: StudentInstitutesMinDetailInterface) {
    this.deleteInvitationSubscription = this.uiService.dialogData$.subscribe(
      result => {
        if (result === true) {
          this.declineInvitation(institute);
        }
        this.deleteInvitationSubscription.unsubscribe();
      }
    )
    this.uiService.openDialog(
      'Do you really want to decline invitation to join \'' + institute.name +  '\'?',
      'No',
      'Yes'
    );
  }

  declineInvitation(institute: StudentInstitutesMinDetailInterface) {
    this.instituteJoinDeclineError = null;
    // this.instituteApiService.acceptDeleteInstituteJoinInvitation(institute.institute_slug, 'DELETE').subscribe(
    //   (result: StatusResponse) => {
    //     if (result.status === 'DELETED') {
    //       this.instituteInvites.splice(this.instituteInvites.indexOf(institute), 1);
    //       this.uiService.showSnackBar(
    //         'Institute join request declined!',  2000
    //       );
    //     }
    //   },
    //   error => {
    //     if (error.error) {
    //       if (error.error.error) {
    //         this.instituteJoinDeclineError = error.error.error;
    //       } else {
    //         this.instituteJoinDeclineError = 'Unable to process request. Refresh and try again.';
    //       }
    //     }
    //   }
    // )
  }

  decodeCountry(key: string) {
    return COUNTRY[key];
  }

  decodeState(key: string) {
    return STATE[key];
  }

  decodeCategory(key: string) {
    return INSTITUTE_CATEGORY[key];
  }

  closeJoinDeclineError() {
    this.instituteJoinDeclineError = null;
  }

  ngOnDestroy() {
    if (this.deleteInvitationSubscription) {
      this.deleteInvitationSubscription.unsubscribe();
    }
  }
}
