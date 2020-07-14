import { Component, OnInit } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';
import { InstituteApiService } from 'src/app/institute-api.service';

interface UserInviteMinDetails {
  email: string;
  image: string;
  invitation_id: number;
  user_id: number;
}

interface InstituteAdminListResponse {
  active_admin_list: UserInviteMinDetails[];
  pending_admin_invites: UserInviteMinDetails[];
}

interface InstituteStaffListResponse {
  active_staff_list: UserInviteMinDetails[];
  pending_staff_invites: UserInviteMinDetails[];
}

interface InstituteFacultyListResponse {
  active_faculty_list: UserInviteMinDetails[];
  pending_faculty_invites: UserInviteMinDetails[];
}


@Component({
  selector: 'app-permissions',
  templateUrl: './permissions.component.html',
  styleUrls: ['./permissions.component.css']
})
export class PermissionsComponent implements OnInit {

  mobileQuery: MediaQueryList;

  // For storing opened expansion panel
  activeAdminStep: number;
  pendingAdminStep: number;
  activeStaffStep: number;
  pendingStaffStep: number;
  activeFacultyStep: number;
  pendingFacultyStep: number;

  // For fetching appropriate data
  instituteSlug: string;
  selectedTab = 'ADMIN';
  inviteError: string;
  invitedSuccessfully: string;

  // For storing data of permitted user
  activeAdminList: UserInviteMinDetails[] = []
  inactiveAdminList: UserInviteMinDetails[] = []
  activeStaffList: UserInviteMinDetails[] = []
  inactiveStaffList: UserInviteMinDetails[] = []
  activeFacultyList: UserInviteMinDetails[] = []
  inactiveFacultyList: UserInviteMinDetails[] = []

  constructor( private media: MediaMatcher,
               private instituteApiService: InstituteApiService) {
    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');
  }

  getAdminUserList() {
    this.instituteApiService.getUserList(this.instituteSlug, 'admin').subscribe(
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
    )
  }

  getStaffUserList() {
    this.instituteApiService.getUserList(this.instituteSlug, 'staff').subscribe(
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
    this.instituteApiService.getUserList(this.instituteSlug, 'faculty').subscribe(
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
    this.instituteSlug = localStorage.getItem('currentInstituteSlug');
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
