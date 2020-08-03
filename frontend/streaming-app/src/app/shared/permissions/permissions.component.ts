import { UserActiveInviteMinDetails, UserPendingInviteMinDetails, InstituteAdminListResponse, InstituteStaffListResponse, InstituteFacultyListResponse } from './../../models/permission.model';
import { Component, OnInit } from '@angular/core';
import { INSTITUTE_ROLE_REVERSE } from 'src/constants';
import { Validators, FormGroup, FormBuilder } from '@angular/forms';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { MediaMatcher } from '@angular/cdk/layout';


@Component({
  selector: 'app-permissions',
  templateUrl: './permissions.component.html',
  styleUrls: ['./permissions.component.css']
})
export class PermissionsComponent implements OnInit {
  mq: MediaQueryList;

  // For storing opened expansion panel
  activeAdminStep: number;
  pendingAdminStep: number;
  activeStaffStep: number;
  pendingStaffStep: number;
  activeFacultyStep: number;
  pendingFacultyStep: number;

  // For fetching appropriate data
  currentInstituteSlug: string;
  currentInstituteRole: string;
  selectedTab = 'ADMIN';
  inviteError: string;
  invitedSuccessfully: string;
  newInviteForm: FormGroup;

  // For storing data of permitted user
  activeAdminList: UserActiveInviteMinDetails[] = []
  inactiveAdminList: UserPendingInviteMinDetails[] = []
  activeStaffList: UserActiveInviteMinDetails[] = []
  inactiveStaffList: UserPendingInviteMinDetails[] = []
  activeFacultyList: UserActiveInviteMinDetails[] = []
  inactiveFacultyList: UserPendingInviteMinDetails[] = []

  constructor( private media: MediaMatcher,
               private instituteApiService: InstituteApiService,
               private formBuilder: FormBuilder ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  getAdminUserList() {
    this.instituteApiService.getUserList(this.currentInstituteSlug, 'admin').subscribe(
      (result: InstituteAdminListResponse) => {
        if (result.active_admin_list){
          for(const activeAdmin of result.active_admin_list) {
            this.activeAdminList.push(activeAdmin);
          }
        }
        if (result.pending_admin_invites) {
          for(const pendingAdminList of result.pending_admin_invites) {
            this.inactiveAdminList.push(pendingAdminList);
          }
        }
      },
      errors => {}
    );

    this.newInviteForm = this.formBuilder.group({
      invitee: [null, [Validators.required, Validators.email]]
    })
  }

  getStaffUserList() {
    this.instituteApiService.getUserList(this.currentInstituteSlug, 'staff').subscribe(
      (result: InstituteStaffListResponse) => {
        if (result.active_staff_list){
          for(const activeStaff of result.active_staff_list) {
            this.activeStaffList.push(activeStaff);
          }
        }
        if (result.pending_staff_invites) {
          for(const pendingStaff of result.pending_staff_invites) {
            this.inactiveStaffList.push(pendingStaff);
          }
        }
      },
      errors => {}
    )
  }

  getFacultyUserList() {
    this.instituteApiService.getUserList(this.currentInstituteSlug, 'faculty').subscribe(
      (result: InstituteFacultyListResponse) => {
        if (result.active_faculty_list){
          for(const activeFaculty of result.active_faculty_list) {
            this.activeFacultyList.push(activeFaculty);
          }
        }
        if (result.pending_faculty_invites) {
          for(const pendingFaculty of result.pending_faculty_invites) {
            this.inactiveFacultyList.push(pendingFaculty);
          }
        }
      },
      errors => {}
    )
  }

  ngOnInit(): void {
    this.currentInstituteSlug = sessionStorage.getItem('currentInstituteSlug');
    this.currentInstituteRole = sessionStorage.getItem('currentInstituteRole');
    this.getAdminUserList();
  }

  clickedTab(event: any){
    if (this.selectedTab === 'ADMIN') {
      this.activeAdminList = [];
      this.inactiveAdminList = [];
    } else if (this.selectedTab === 'STAFF') {
      this.activeStaffList = [];
      this.inactiveStaffList = [];
    } else {
      this.activeFacultyList = [];
      this.inactiveFacultyList = [];
    }
    this.newInviteForm.reset();
    this.inviteError = null;
    this.invitedSuccessfully = null;

    if (event.index === 0) {
      this.selectedTab = 'ADMIN';
      this.getAdminUserList();
    } else if (event.index === 1) {
      this.selectedTab = 'STAFF';
      this.getStaffUserList();
    } else {
      this.selectedTab = 'FACULTY';
      this.getFacultyUserList();
    }
  }


  inviteUser() {
    this.inviteError = null;
    this.invitedSuccessfully = null;
    let payload = {
      "invitee": this.newInviteForm.value.invitee,
      "role": ""
    }
    if (this.selectedTab === 'STAFF') {
      payload["role"] = INSTITUTE_ROLE_REVERSE['Staff'];
    } else if (this.selectedTab === 'FACULTY') {
      payload["role"] = INSTITUTE_ROLE_REVERSE['Faculty'];
    } else {
      payload["role"] = INSTITUTE_ROLE_REVERSE['Admin'];
    }
    this.instituteApiService.inviteUser(this.currentInstituteSlug, payload).subscribe(
      (result: UserPendingInviteMinDetails) => {
        this.invitedSuccessfully = 'User has been invited successfully.'
        this.newInviteForm.reset();
        if (this.selectedTab === 'STAFF') {
          this.inactiveStaffList.push(result);
        } else if (this.selectedTab === 'FACULTY') {
          this.inactiveFacultyList.push(result);
        } else {
          this.inactiveAdminList.push(result);
        }
      },
      error => {
        if (error.error.invitee) {
          this.inviteError = error.error.invitee;
        } else if (error.error.error) {
          this.inviteError = error.error.get('error');
        } else {
          this.inviteError = 'Invitation failed. Check internet connectivity.'
        }
      }
    )
  }

  // For handling mat expansion panel
  setActiveAdminPanelStep(step: number) {
    this.activeAdminStep = step;
  }

  setPendingAdminPanelStep(step: number) {
    this.pendingAdminStep = step;
  }

  setActiveStaffPanelStep(step: number) {
    this.activeStaffStep = step;
  }

  setPendingStaffPanelStep(step: number) {
    this.pendingStaffStep = step;
  }

  setActiveFacultyPanelStep(step: number) {
    this.activeFacultyStep = step;
  }

  setPendingFacultyPanelStep(step: number) {
    this.pendingFacultyStep = step;
  }

  isActiveAdminListEmpty() {
    return this.activeAdminList.length === 0;
  }

  isInactiveAdminListEmpty() {
    return this.inactiveAdminList.length === 0;
  }

  isActiveStaffListEmpty() {
    return this.activeStaffList.length === 0;
  }

  isInactiveStaffListEmpty() {
    return this.inactiveStaffList.length === 0;
  }

  isActiveFacultyListEmpty() {
    return this.activeFacultyList.length === 0;
  }

  isInactiveFacultyListEmpty() {
    return this.inactiveFacultyList.length === 0;
  }
}
