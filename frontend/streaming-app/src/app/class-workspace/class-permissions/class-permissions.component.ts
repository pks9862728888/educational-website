import { currentInstituteSlug, currentClassSlug, currentInstituteRole } from './../../../constants';
import { Component, OnInit } from '@angular/core';
import { Validators, FormGroup, FormBuilder } from '@angular/forms';
import { MediaMatcher } from '@angular/cdk/layout';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { ClassPermittedUserDetails } from 'src/app/models/class.model';

@Component({
  selector: 'app-class-permissions',
  templateUrl: './class-permissions.component.html',
  styleUrls: ['./class-permissions.component.css']
})
export class ClassPermissionsComponent implements OnInit {

  mq: MediaQueryList;
  activeInchargeStep: number;
  currentInstituteSlug: string;
  currentInstituteRole: string;
  currentClassSlug: string;
  errorText: string;
  successText: string;
  newInviteForm: FormGroup;
  createInviteIndicator: boolean;
  showInviteFormMb: boolean;
  showLoadingIndicator: boolean;
  loadingText = 'Fetching Class Incharge Details...';
  showReloadError: boolean;
  showReloadText = 'Unable to fetch class incharge details!';
  inchargeList: ClassPermittedUserDetails[];

  constructor(
    private media: MediaMatcher,
    private instituteApiService: InstituteApiService,
    private formBuilder: FormBuilder ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.currentInstituteRole = sessionStorage.getItem(currentInstituteRole);
    this.currentClassSlug = sessionStorage.getItem(currentClassSlug);
  }

  ngOnInit(): void {
    this.getInchargeList();
    this.newInviteForm = this.formBuilder.group({
      invitee: [null, [Validators.required, Validators.email]]
    });
  }

  getInchargeList() {
    this.showLoadingIndicator = true;
    this.showReloadError = false;
    this.errorText = null;
    this.successText = null;
    this.instituteApiService.getClassInchargeList(this.currentClassSlug).subscribe(
      (result: ClassPermittedUserDetails[]) => {
        this.showLoadingIndicator = false;
        this.inchargeList = result;
      },
      errors => {
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
    )
  }

  invite() {
    this.errorText = null;
    this.successText = null;
    this.createInviteIndicator = true;
    this.instituteApiService.addClassIncharge(this.newInviteForm.value.invitee,
                                              this.currentClassSlug).subscribe(
        (result: ClassPermittedUserDetails) => {
          this.createInviteIndicator = false;
          if (!this.inchargeList) {
            this.inchargeList = [];
          }
          this.inchargeList.push(result);
          this.successText = 'User invited successfully.';
        },
        errors => {
          this.createInviteIndicator = false;
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

  closeSuccessText() {
    this.successText = null;
  }
}
