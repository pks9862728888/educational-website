import { INSTITUTE_ROLE_REVERSE } from 'src/constants';
import { InstituteStudentResponse, InstituteBannedStudentMinDetails, InstituteBannedStudentResponse } from './../../models/student.model';
import { Subscription } from 'rxjs';
import { UiService } from './../../services/ui.service';
import { currentInstituteSlug, GENDER_FORM_FIELD_OPTIONS, GENDER, currentInstituteRole } from './../../../constants';
import { InstituteApiService } from '../../services/institute-api.service';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { ClassSlugNameResponse } from '../../models/class.model';
import { InstituteStudentMinDetails } from '../../models/student.model';
import { formatDate } from '../../format-datepicker';

@Component({
  selector: 'app-institute-students',
  templateUrl: './institute-students.component.html',
  styleUrls: ['./institute-students.component.css']
})
export class InstituteStudentsComponent implements OnInit {

  mq: MediaQueryList;
  maxDate: Date;
  genderOptions = GENDER_FORM_FIELD_OPTIONS;
  currentInstituteSlug: string;
  currentInstituteRole: string;

  showInvitationForm: boolean;
  invitationForm: FormGroup;
  showInvitingIndicator: boolean;
  inviteError: string;

  invitedStudentsStep: number;
  invitedStudentsLoadingIndicator: boolean;
  showInvitedStudentsReload: boolean;
  invitedStudentsGetError: string;
  invitedStudentEditIndex: number;
  deleteInvitedStudentSubscription: Subscription;

  activeStudentsStep: number;
  activeStudentsLoadingIndicator: boolean;
  showActiveStudentsReload: boolean;
  activeStudentsGetError: string;
  activeStudentEditIndex: number;
  deleteActiveStudentSubscription: Subscription;

  bannedStudentsStep: number;
  bannedStudentsLoadingIndicator: boolean;
  showBannedStudentsReload: boolean;
  bannedStudentsGetError: string;
  bannedStudentEditIndex: number;
  removeBannedStudentSubscription: Subscription;

  invitedStudents: InstituteStudentMinDetails[] = [];
  activeStudents: InstituteStudentMinDetails[] = [];
  bannedStudents: InstituteBannedStudentMinDetails[] = [];
  classes: ClassSlugNameResponse[] = [];

  constructor(
    private media: MediaMatcher,
    private formBuilder: FormBuilder,
    private instituteApiService: InstituteApiService,
    private uiService: UiService
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.maxDate = new Date();
  }

  ngOnInit(): void {
    this.invitationForm = this.formBuilder.group({
      invitee_email: ['', [Validators.required, Validators.email]],
      first_name: ['', [Validators.maxLength(30)]],
      last_name: ['', [Validators.maxLength(30)]],
      registration_no: ['', [Validators.maxLength(15)]],
      enrollment_no: ['', [Validators.maxLength(15)]],
      gender: [''],
      date_of_birth: [],
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
      (result: InstituteStudentResponse) => {
        this.invitedStudentsLoadingIndicator = false;
        this.invitedStudents = result.data;
        this.currentInstituteRole = result.requester_role
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
      (result: InstituteStudentResponse) => {
        this.activeStudentsLoadingIndicator = false;
        this.activeStudents = result.data;
        this.currentInstituteRole = result.requester_role
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
    this.instituteApiService.getInstituteStudentsList(
      this.currentInstituteSlug,
      'banned'
    ).subscribe(
      (result: InstituteBannedStudentResponse) => {
        this.bannedStudentsLoadingIndicator = false;
        this.bannedStudents = result.data;
        this.currentInstituteRole = result.requester_role
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
    if (data.date_of_birth) {
      // Formatting date of birth in YYYY-MM-DD
      data.date_of_birth = formatDate(data.date_of_birth);
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

  setBannedStudentsStep(step: number) {
    this.bannedStudentsStep = step;
    if (this.bannedStudentEditIndex !== null && this.bannedStudentEditIndex !== undefined) {
      this.hideBannedStudentEditForm();
    }
  }

  tabChanged(activeTab) {
    this.invitedStudentsStep = null;
    this.activeStudentsStep = null;
    this.bannedStudentsStep = null;
    this.invitedStudentEditIndex = null;
    this.activeStudentEditIndex = null;
    this.bannedStudentEditIndex = null;
    if (activeTab.index === 0) {
      this.getInvitedStudentsList();
    } else if (activeTab.index === 1) {
      this.getActiveStudentsList();
    } else {
      this.getBannedStudentsList();
    }
  }

  editInvitedStudentDetails(index: number) {
    this.invitedStudentEditIndex = index;
    this.invitedStudents[index]['edit'] = true;
  }

  editActiveStudentDetails(index: number) {
    this.activeStudentEditIndex = index;
    this.activeStudents[index]['edit'] = true;
  }

  editBannedStudentDetails(index: number) {
    this.bannedStudentEditIndex = index;
    this.bannedStudents[index]['edit'] = true;
  }

  hideInvitedStudentEditForm() {
    this.invitedStudents[this.invitedStudentEditIndex]['edit'] = false;
    this.invitedStudentEditIndex = null;
  }

  hideActiveStudentEditForm() {
    this.activeStudents[this.activeStudentEditIndex]['edit'] = false;
    this.activeStudentEditIndex = null;
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
      'Do you really want to unban student \'' + name + '\'?',
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

  userIsAdmin() {
    if (this.currentInstituteRole === INSTITUTE_ROLE_REVERSE['Admin']) {
      return true;
    } else {
      return false;
    }
  }
}
