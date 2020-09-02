import { Subscription } from 'rxjs';
import { UiService } from './../../services/ui.service';
import { currentInstituteSlug } from './../../../constants';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { ClassSlugNameResponse } from 'src/app/models/class.model';
import { InstituteStudentMinDetails } from '../../models/student.model';

@Component({
  selector: 'app-invite-students',
  templateUrl: './invite-students.component.html',
  styleUrls: ['./invite-students.component.css']
})
export class InviteStudentsComponent implements OnInit {

  mq: MediaQueryList;
  currentInstituteSlug: string;
  invitedStudentsStep: number;
  activeStudentsStep: number;
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
  activeStudentEditIndex: number;
  invitedStudentEditIndex: number;

  deleteInvitedStudentSubscription: Subscription;
  deleteActiveStudentSubscription: Subscription;

  invitedStudents: InstituteStudentMinDetails[] = [];
  activeStudents: InstituteStudentMinDetails[] = [];
  classes: ClassSlugNameResponse[] = [];

  constructor(
    private media: MediaMatcher,
    private formBuilder: FormBuilder,
    private instituteApiService: InstituteApiService,
    private uiService: UiService
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
  }

  ngOnInit(): void {
    this.invitationForm = this.formBuilder.group({
      invitee_email: ['', [Validators.required, Validators.email]],
      first_name: ['', [Validators.maxLength(30)]],
      last_name: ['', [Validators.maxLength(30)]],
      registration_no: ['', [Validators.maxLength(15)]],
      enrollment_no: ['', [Validators.maxLength(15)]],
      class: []
    });
    this.getClassList();
    this.getInvitedStudentsList();
  }

  getInvitedStudentsList() {
    this.invitedStudentsLoadingIndicator = true;
    this.showInvitedStudentsReload = false;
    this.instituteApiService.getInstituteStudentsList(
      this.currentInstituteSlug,
      'inactive'
    ).subscribe(
      (result: InstituteStudentMinDetails[]) => {
        this.invitedStudentsLoadingIndicator = false;
        this.invitedStudents = result;
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
    this.instituteApiService.getInstituteStudentsList(
      this.currentInstituteSlug,
      'active'
    ).subscribe(
      (result: InstituteStudentMinDetails[]) => {
        this.activeStudentsLoadingIndicator = false;
        this.activeStudents = result;
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

  invite() {
    let data = this.invitationForm.value;
    if (!data.first_name) {
      data.first_name = '';
    }
    if (!data.last_name) {
      data.last_name = '';
    }
    if (!data.enrollment_no) {
      data.enrollment_no = '';
    }
    if (!data.registration_no) {
      data.registration_no = '';
    }
    if (this.classes.length === 0) {
      delete data['class'];
    }
    this.showInvitingIndicator = true;
    this.closeInviteError();
    this.invitationForm.disable();
    this.instituteApiService.inviteStudentToInstitute(
      this.currentInstituteSlug,
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
        this.invitedStudents.unshift(result);
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

  getClassList() {
    this.instituteApiService.getInstituteClassKeyValuePairs(
      this.currentInstituteSlug
    ).subscribe(
      (result: ClassSlugNameResponse[]) => {
        this.classes = result;
        this.patchClassToForm();
      }
    );
  }

  patchClassToForm() {
    if (this.classes.length > 0) {
      this.invitationForm.patchValue({
        class: this.classes[0].class_slug
      });
    }
  }

  showInviteForm() {
    this.closeInviteError();
    this.patchClassToForm();
    this.showInvitationForm = true;
  }

  hideInviteForm() {
    this.resetInviteForm();
    this.showInvitationForm = false;
  }

  resetInviteForm() {
    this.closeInviteError();
    this.invitationForm.reset();
    this.patchClassToForm();
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

  tabChanged(activeTab) {
    this.activeStudentsStep = null;
    this.invitedStudentsStep = null;
    this.activeStudentEditIndex = null;
    this.invitedStudentEditIndex = null;
    if (activeTab.index === 0) {
      this.getInvitedStudentsList();
    } else {
      this.getActiveStudentsList();
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

  hideActiveStudentEditForm() {
    this.activeStudents[this.activeStudentEditIndex]['edit'] = false;
    this.activeStudentEditIndex = null;
  }

  hideInvitedStudentEditForm() {
    this.invitedStudents[this.invitedStudentEditIndex]['edit'] = false;
    this.invitedStudentEditIndex = null;
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

  userIsAdmin() {

  }
}
