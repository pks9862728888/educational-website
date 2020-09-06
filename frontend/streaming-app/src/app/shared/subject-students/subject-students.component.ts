import { InstituteStudentResponse, InstituteBannedStudentResponse } from './../../models/student.model';
import { INSTITUTE_ROLE_REVERSE } from 'src/constants';
import { currentSubjectSlug, currentInstituteRole, hasClassPerm } from './../../../constants';
import { Component, OnInit } from '@angular/core';
import { GENDER, currentInstituteSlug, currentClassSlug, GENDER_FORM_FIELD_OPTIONS } from '../../../constants';
import { InstituteBannedStudentMinDetails, InstituteStudentMinDetails } from '../../models/student.model';
import { Validators, FormBuilder, FormGroup } from '@angular/forms';
import { UiService } from 'src/app/services/ui.service';
import { InstituteApiService } from '../../services/institute-api.service';
import { MediaMatcher } from '@angular/cdk/layout';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-subject-students',
  templateUrl: './subject-students.component.html',
  styleUrls: ['./subject-students.component.css']
})
export class SubjectStudentsComponent implements OnInit {

  mq: MediaQueryList;
  maxDate: Date;
  genderOptions = GENDER_FORM_FIELD_OPTIONS;
  currentInstituteSlug: string;
  currentClassSlug: string;
  currentSubjectSlug: string;
  currentInstituteRole: string;
  hasPerm: boolean;

  invitedStudentsStep: number;
  activeStudentsStep: number;
  bannedStudentsStep: number;

  showInvitationForm: boolean;
  invitationForm: FormGroup;
  showInvitingIndicator: boolean;
  inviteError: string;

  invitedStudentsLoadingIndicator: boolean;
  showInvitedStudentsReload: boolean;
  invitedStudentsGetError: string;
  invitedStudentEditIndex: number;

  activeStudentsLoadingIndicator: boolean;
  showActiveStudentsReload: boolean;
  activeStudentsGetError: string;
  activeStudentEditIndex: number;

  bannedStudentsLoadingIndicator: boolean;
  showBannedStudentsReload: boolean;
  bannedStudentsGetError: string;
  bannedStudentEditIndex: number;

  deleteInvitedStudentSubscription: Subscription;
  deleteActiveStudentSubscription: Subscription;
  removeBannedStudentSubscription: Subscription;

  invitedStudents: InstituteStudentMinDetails[] = [];
  activeStudents: InstituteStudentMinDetails[] = [];
  bannedStudents: InstituteBannedStudentMinDetails[] = [];

  constructor(
    private media: MediaMatcher,
    private formBuilder: FormBuilder,
    private instituteApiService: InstituteApiService,
    private uiService: UiService
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.currentClassSlug = sessionStorage.getItem(currentClassSlug);
    this.currentSubjectSlug = sessionStorage.getItem(currentSubjectSlug);
    this.maxDate = new Date();
  }

  ngOnInit(): void {
    this.invitationForm = this.formBuilder.group({
      invitee_email: ['', [Validators.required, Validators.email]]
    });
    this.getInvitedStudentsList();
  }

  getInvitedStudentsList() {
    this.invitedStudentsLoadingIndicator = true;
    this.showInvitedStudentsReload = false;
    this.instituteApiService.getSubjectStudentsList(
      this.currentInstituteSlug,
      this.currentClassSlug,
      this.currentSubjectSlug,
      'inactive'
    ).subscribe(
      (result: InstituteStudentResponse) => {
        this.invitedStudentsLoadingIndicator = false;
        this.invitedStudents = result.data;
        this.currentInstituteRole = result.requester_role;
        this.hasPerm = result.has_perm;
      },
      errors => {
        this.invitedStudentsLoadingIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.invitedStudentsGetError = errors.error.error;
          } else {
            this.showInvitedStudentsReload = true;
          }
        } else {
          this.showInvitedStudentsReload = true;
        }
      }
    );
  }

  getActiveStudentsList() {
    this.activeStudentsLoadingIndicator = true;
    this.showActiveStudentsReload = false;
    this.instituteApiService.getSubjectStudentsList(
      this.currentInstituteSlug,
      this.currentClassSlug,
      this.currentSubjectSlug,
      'active'
    ).subscribe(
      (result: InstituteStudentResponse) => {
        this.activeStudents = result.data;
        this.currentInstituteRole = result.requester_role;
        this.activeStudentsLoadingIndicator = false;
        this.hasPerm = result.has_perm;
      },
      errors => {
        this.activeStudentsLoadingIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.activeStudentsGetError = errors.error.error;
          } else {
            this.showActiveStudentsReload = true;
          }
        } else {
          this.showActiveStudentsReload = true;
        }
      }
    );
  }

  getBannedStudentsList() {
    this.bannedStudentsLoadingIndicator = true;
    this.showBannedStudentsReload = false;
    this.instituteApiService.getSubjectStudentsList(
      this.currentInstituteSlug,
      this.currentClassSlug,
      this.currentSubjectSlug,
      'banned'
    ).subscribe(
      (result: InstituteBannedStudentResponse) => {
        this.bannedStudentsLoadingIndicator = false;
        this.bannedStudents = result.data;
        this.currentInstituteRole = result.requester_role;
        this.hasPerm = result.has_perm;
      },
      errors => {
        this.bannedStudentsLoadingIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.bannedStudentsGetError = errors.error.error;
          } else {
            this.showBannedStudentsReload = true;
          }
        } else {
          this.showBannedStudentsReload = true;
        }
      }
    );
  }

  invite() {
    let data = this.invitationForm.value;
    this.showInvitingIndicator = true;
    this.closeInviteError();
    this.invitationForm.disable();
    this.instituteApiService.inviteStudentToSubject(
      this.currentInstituteSlug,
      this.currentClassSlug,
      this.currentSubjectSlug,
      data
    ).subscribe(
      (result: InstituteStudentMinDetails) => {
        this.invitationForm.enable();
        this.invitationForm.reset();
        this.showInvitingIndicator = false;
        this.uiService.showSnackBar(
          'User invited Successfully!',
          2000
        );
        this.showInvitationForm = false;
        if (result.active) {
          this.activeStudents.unshift(result);
        } else{
          this.invitedStudents.unshift(result);
        }
      },
      errors => {
        this.invitationForm.enable();
        this.showInvitingIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.inviteError = errors.error.error;
          } else {
            this.inviteError = 'Unable to invite. Please refresh and try again.';
          }
        } else {
          this.inviteError = 'Unable to invite. Please refresh and try again.';
        }
      }
    );
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
    if (this.invitedStudentEditIndex !== null && this.invitedStudentEditIndex !== undefined) {
      this.hideInvitedStudentEditForm();
    }
  }

  setActiveStudentsStep(step: number) {
    this.activeStudentsStep = step;
    if (this.activeStudentEditIndex !== null && this.activeStudentEditIndex !== undefined) {
      this.hideActiveStudentEditForm();
    }
  }

  setBannedStudentsStep(step: number) {
    this.bannedStudentsStep = step;
    if (this.bannedStudentEditIndex !== null && this.bannedStudentEditIndex !== undefined) {
      this.hideBannedStudentEditForm();
    }
  }

  tabChanged(activeTab) {
    this.activeStudentsStep = null;
    this.invitedStudentsStep = null;
    this.bannedStudentsStep = null;
    this.activeStudentEditIndex = null;
    this.invitedStudentEditIndex = null;
    this.bannedStudentEditIndex = null;
    if (activeTab.index === 0) {
      this.getInvitedStudentsList();
    } else if (activeTab.index === 1) {
      this.getActiveStudentsList();
    } else {
      this.getBannedStudentsList();
    }
  }

  editActiveStudentDetails(index: number) {
    this.activeStudentEditIndex = index;
    this.activeStudents[index]['edit'] = true;
  }

  editInvitedStudentDetails(index: number) {
    this.invitedStudentEditIndex = index;
    this.invitedStudents[index]['edit'] = true;
  }

  editBannedStudentDetails(index: number) {
    this.bannedStudentEditIndex = index;
    this.bannedStudents[index]['edit'] = true;
  }

  hideActiveStudentEditForm() {
    this.activeStudents[this.activeStudentEditIndex]['edit'] = false;
    this.activeStudentEditIndex = null;
  }

  hideInvitedStudentEditForm() {
    this.invitedStudents[this.invitedStudentEditIndex]['edit'] = false;
    this.invitedStudentEditIndex = null;
  }

  hideBannedStudentEditForm() {
    this.bannedStudents[this.bannedStudentEditIndex]['edit'] = false;
    this.bannedStudentEditIndex = null;
  }

  updateActiveStudentData(studentData: InstituteStudentMinDetails) {
    this.activeStudents.splice(
      this.activeStudentEditIndex,
      1,
      studentData
    );
    this.uiService.showSnackBar(
      'Updated student data successfully!',
      2000
    );
    this.hideActiveStudentEditForm();
  }

  updateInvitedStudentData(studentData: InstituteStudentMinDetails) {
    this.invitedStudents.splice(
      this.invitedStudentEditIndex,
      1,
      studentData
    );
    this.uiService.showSnackBar(
      'Updated student data successfully!',
      2000
    );
    this.hideInvitedStudentEditForm();
  }

  updateBannedStudentData(studentData: InstituteBannedStudentMinDetails) {
    this.bannedStudents.splice(
      this.bannedStudentEditIndex,
      1,
      studentData
    );
    this.uiService.showSnackBar(
      'Updated student data successfully!',
      2000
    );
    this.hideBannedStudentEditForm();
  }

  deleteInvitedStudentConfirm(index: number) {
    let name = '';
    if (this.invitedStudents[index].first_name) {
      name = this.invitedStudents[index].first_name + ' ' + this.invitedStudents[index].last_name;
      name = name.toUpperCase();
    } else {
      name = this.invitedStudents[index].invitee_email;
    }
    this.deleteInvitedStudentSubscription = this.uiService.dialogData$.subscribe(
      (data) => {
        if (data === true) {
          this.deleteInvitedStudent(index);
        }
        this.deleteInvitedStudentSubscription.unsubscribe();
      }
    );
    this.uiService.openDialog(
      'Are you sure you want to remove student \'' + name + '\'?',
      'No',
      'Yes'
    );
  }

  deleteInvitedStudent(index: number) {
    this.invitedStudents[index]['delete'] = true;
    console.log(index);
  }

  deleteActiveStudentConfirm(index: number) {
    let name = '';
    if (this.activeStudents[index].first_name) {
      name = this.activeStudents[index].first_name + ' ' + this.activeStudents[index].last_name;
      name = name.toUpperCase();
    } else {
      name = this.activeStudents[index].invitee_email;
    }
    this.deleteActiveStudentSubscription = this.uiService.dialogData$.subscribe(
      (data) => {
        if (data === true) {
          this.deleteActiveStudent(index);
        }
        this.deleteActiveStudentSubscription.unsubscribe();
      }
    );
    this.uiService.openDialog(
      'Are you sure you want to remove student \'' + name + '\'?',
      'No',
      'Yes'
    );
  }

  deleteActiveStudent(index: number) {
    this.activeStudents[index]['delete'] = true;
    console.log(index);
  }

  removeBannedStudentConfirm(index: number) {
    let name = '';
    if (this.bannedStudents[index].first_name) {
      name = this.bannedStudents[index].first_name + ' ' + this.bannedStudents[index].last_name;
      name = name.toUpperCase();
    } else {
      name = this.bannedStudents[index].invitee_email;
    }
    this.removeBannedStudentSubscription = this.uiService.dialogData$.subscribe(
      (data) => {
        if (data === true) {
          this.removeBannedStudent(index);
        }
        this.removeBannedStudentSubscription.unsubscribe();
      }
    );
    this.uiService.openDialog(
      'Are you sure you want to unban student \'' + name + '\'?',
      'No',
      'Yes'
    );
  }

  removeBannedStudent(index: number) {
    this.bannedStudents[index]['delete'] = true;
    console.log(index);
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

  isBannedStudentsEmpty() {
    if (this.bannedStudents.length === 0) {
      return true;
    } else {
      return false;
    }
  }

  closeInviteError() {
    this.inviteError = null;
  }

  getGender(key: string) {
    return GENDER[key];
  }

  hasSubjectPerm() {
    if (this.hasPerm || this.currentInstituteRole === INSTITUTE_ROLE_REVERSE['Admin']) {
      return true;
    } else {
      return false;
    }
  }

  userIsStaff() {
    if (this.currentInstituteRole === INSTITUTE_ROLE_REVERSE['Staff']) {
      return true;
    } else {
      return false;
    }
  }
}
