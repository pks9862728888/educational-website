import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'app-invite-students',
  templateUrl: './invite-students.component.html',
  styleUrls: ['./invite-students.component.css']
})
export class InviteStudentsComponent implements OnInit {

  mq: MediaQueryList;
  invitedStudentsStep: number;
  invitedStudents = [];
  activeStudents = [];
  showInvitationForm: boolean;
  invitationForm: FormGroup;
  showInvitingIndicator: boolean;
  inviteError: string;
  invitedStudentsLoadingIndicator: boolean;
  showInvitedStudentsReload: boolean;
  invitedStudentsGetError: string;
  activeStudentsLoadingIndicator: boolean;
  showActiveStudentsReload: boolean;
  activeStudentsGetError: string;

  constructor(
    private media: MediaMatcher,
    private formBuilder: FormBuilder
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.invitationForm = this.formBuilder.group({
      email: [null, [Validators.required]],
      first_name: [null, [Validators.maxLength(30)]],
      last_name: [null, [Validators.maxLength(30)]],
      registration_no: [null, [Validators.maxLength(15)]],
      enrollment_no: [null, [Validators.maxLength(15)]]
    });
    this.getInvitedStudentsList();
  }

  invite() {
    console.log(this.invitationForm.value);
  }

  getInvitedStudentsList() {

  }

  getActiveStudentsList() {

  }

  showInviteForm() {
    this.closeInviteError();
    this.showInvitationForm = true;
  }

  hideInviteForm() {
    this.resetInviteForm();
    this.showInvitationForm = false;
  }

  resetInviteForm() {
    this.closeInviteError();
    this.invitationForm.reset();
  }

  setInvitedStudentsStep(step: number) {
    this.invitedStudentsStep = step;
  }

  isInvitedStudentsEmpty() {
    if (this.invitedStudents.length === 0) {
      return true;
    } else {
      return false;
    }
  }

  isActiveStudentsEmpty() {
    if (this.activeStudents.length === 0) {
      return true;
    } else {
      return false;
    }
  }

  closeInviteError() {
    this.inviteError = null;
  }

}
