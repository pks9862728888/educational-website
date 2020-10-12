import { currentInstituteSlug,
         currentInstituteRole,
         currentSubjectSlug,
         hasClassPerm,
         INSTITUTE_ROLE_REVERSE,
         userId,
         hasSubjectPerm } from './../../../constants';
import { Component, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { MediaMatcher } from '@angular/cdk/layout';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { SubjectPermittedUserDetails } from '../../models/subject.model';
import { UiService } from 'src/app/services/ui.service';

@Component({
  selector: 'app-subject-permission',
  templateUrl: './subject-permission.component.html',
  styleUrls: ['./subject-permission.component.css']
})
export class SubjectPermissionComponent implements OnInit {

  mq: MediaQueryList;
  userId: string;
  hasClassPerm: boolean;
  activeInchargeStep: number;
  currentInstituteSlug: string;
  currentInstituteRole: string;
  currentSubjectSlug: string;
  errorText: string;
  createInviteIndicator: boolean;
  showInviteFormMb: boolean;
  showLoadingIndicator: boolean;
  loadingText = 'Fetching Subject Incharge Details...';
  showReloadError: boolean;
  showReloadText = 'Unable to fetch subject incharge details!';
  inputPlaceholder = 'Email of invitee';
  inviteButtonText = 'Invite';
  progressSpinnerText = 'Inviting user...';
  inchargeList: SubjectPermittedUserDetails[];
  formEvent = new Subject<string>();

  constructor(
    private media: MediaMatcher,
    private instituteApiService: InstituteApiService,
    private uiService: UiService
    ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.userId = sessionStorage.getItem('user_id');
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.currentInstituteRole = sessionStorage.getItem(currentInstituteRole);
    this.currentSubjectSlug = sessionStorage.getItem(currentSubjectSlug);

    if (sessionStorage.getItem(hasClassPerm) === 'true') {
      this.hasClassPerm = true;
    } else {
      this.hasClassPerm = false;
    }
  }

  ngOnInit(): void {
    this.getInchargeList();
  }

  getInchargeList() {
    this.showLoadingIndicator = true;
    this.showReloadError = false;
    this.errorText = null;
    this.instituteApiService.getInstituteSubjectInchargeList(this.currentSubjectSlug).subscribe(
      (result: SubjectPermittedUserDetails[]) => {
        this.showLoadingIndicator = false;
        this.inchargeList = result;
      },
      (errors: any) => {
        this.showLoadingIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.errorText = errors.error.error;
          } else {
            this.showReloadError = true;
          }
        } else {
          this.showReloadError = true;
        }
      }
    );
  }

  invite(inviteeEmail: string) {
    this.errorText = null;
    this.createInviteIndicator = true;
    this.formEvent.next('disable');
    this.instituteApiService.addSubjectIncharge(inviteeEmail,
      this.currentSubjectSlug).subscribe(
        (result: SubjectPermittedUserDetails) => {
          this.createInviteIndicator = false;
          this.showReloadError = false;

          if (!this.inchargeList) {
            this.inchargeList = [];
          }

          this.inchargeList.push(result);
          this.formEvent.next('reset');

          if (result.invitee_id.toString() === sessionStorage.getItem(userId)) {
            sessionStorage.setItem(hasSubjectPerm, 'true');
          }

          this.uiService.showSnackBar(
            'User invited successfully!',
            2000
          );
        },
        errors => {
          this.createInviteIndicator = false;
          this.formEvent.next('enable');
          if (errors.error) {
            if (errors.error.error) {
              this.errorText = errors.error.error;
            } else {
              this.errorText = 'Unknown error occured.';
            }
          } else {
            this.errorText = 'Unknown error occured.';
          }
        }
    );
  }

  // For handling mat expansion panel
  setActiveInchargePanelStep(step: number) {
    this.activeInchargeStep = step;
  }

  hasClassIncharge() {
    if (this.inchargeList) {
      return this.inchargeList.length > 0;
    } else {
      return false;
    }
  }

  showInviteFormMobile() {
    this.showInviteFormMb = true;
  }

  hideInviteFormMobile() {
    this.showInviteFormMb = false;
  }

  closeErrorText() {
    this.errorText = null;
  }

  userIsAdmin() {
    if (sessionStorage.getItem(currentInstituteRole) === INSTITUTE_ROLE_REVERSE.Admin) {
      return true;
    } else {
      return false;
    }
  }

  userNotSelf(inviteeId: number) {
    if (inviteeId.toString() !== this.userId) {
      return true;
    } else {
      return false;
    }
  }

}
