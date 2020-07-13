import { Component, OnInit } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';

@Component({
  selector: 'app-permissions',
  templateUrl: './permissions.component.html',
  styleUrls: ['./permissions.component.css']
})
export class PermissionsComponent implements OnInit {

  mobileQuery: MediaQueryList;
  abc = [1, 2];

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

}
