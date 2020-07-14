import { Component, OnInit } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';

@Component({
  selector: 'app-permissions',
  templateUrl: './permissions.component.html',
  styleUrls: ['./permissions.component.css']
})
export class PermissionsComponent implements OnInit {

  mobileQuery: MediaQueryList;
  abc = [1,2];

  // For storing opened expansion panel
  activeAdminStep: number;
  pendingAdminStep: number;
  activeStaffStep: number;
  pendingStaffStep: number;
  activeFacultyStep: number;
  pendingFacultyStep: number;

  // For fetching appropriate data
  selectedTab = 'ADMIN';
  inviteError: string;
  invitedSuccessfully: string;

  constructor( private media: MediaMatcher) {
    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    // this.inviteError = 'This user does not exist.';
    // this.invitedSuccessfully = 'User has been invited.';
  }

  clickedTab(event: any){
    if (event.index === 0) {
      this.selectedTab = 'ADMIN';
    } else if (event.index === 1) {
      this.selectedTab = 'STAFF';
    } else {
      this.selectedTab = 'FACULTY';
    }
    console.log(this.selectedTab);
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

}
