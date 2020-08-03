import { currentInstituteSlug, currentClassSlug, currentInstituteRole } from './../../../constants';
import { Component, OnInit } from '@angular/core';
import { Validators, FormGroup, FormBuilder } from '@angular/forms';
import { MediaMatcher } from '@angular/cdk/layout';
import { InstituteApiService } from 'src/app/services/institute-api.service';

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
  inchargeList = []

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

  }

  invite() {
    this.errorText = null;
    this.successText = null;
    const payload = {
      "invitee": this.newInviteForm.value.invitee,
      "class_slug": 'sdf'
    };
    alert('invite clicked');
  }

  // For handling mat expansion panel
  setActiveInchargePanelStep(step: number) {
    this.activeInchargeStep = step;
  }

  hasClassIncharge() {
    return this.inchargeList.length > 0;
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
