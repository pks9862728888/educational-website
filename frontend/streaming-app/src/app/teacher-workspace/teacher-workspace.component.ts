import { InAppDataTransferService } from '../services/in-app-data-transfer.service';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-teacher-workspace',
  templateUrl: './teacher-workspace.component.html',
  styleUrls: ['./teacher-workspace.component.css']
})
export class TeacherWorkspaceComponent implements OnInit, OnDestroy {

  // For showing sidenav toolbar
  mobileQuery: MediaQueryList;
  opened: boolean;
  activeLink: string;
  showTempNamesSubscription: Subscription;
  tempBreadcrumbLinkName: string;

  constructor( private router: Router,
               private media: MediaMatcher,
               private inAppDataTransferService: InAppDataTransferService ) {

    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');

    // Initializing sidenav active route in case page is reloaded
    const active_route = sessionStorage.getItem('activeRoute');
    if (active_route && (active_route === 'PROFILE' || active_route === 'INSTITUTES' || active_route === 'CHATROOMS')) {
      this.activeLink = active_route;
    } else {
      sessionStorage.setItem('activeRoute', 'PROFILE');
      this.activeLink = 'PROFILE';
    }
  }

  ngOnInit(): void {
    // For keeping the sidenav opened in desktop view in the beginning
    if (this.mobileQuery.matches === true) {
      this.opened = false;
    } else {
      this.opened = true;
    }

    this.showTempNamesSubscription = this.inAppDataTransferService.activeBreadcrumbLinkData$.subscribe(
      (linkName: string) => {
        this.tempBreadcrumbLinkName = linkName;
      }
    );
  }

  // For navigating to teacher-workspace view
  navigate(link: string) {
    if (link !== this.activeLink) {
      this.activeLink = link;

      if (this.activeLink === 'HOME') {
        this.router.navigate(['/home']);
      } else {
        this.router.navigate(['/teacher-workspace/' + link.toLowerCase()]);
      }
    }
  }

  // For navbar
  performAction(link: string) {
    // Hiding navbar if it is mobile
    if (this.mobileQuery.matches === true) {
      this.opened = false;
    }
    this.navigate(link);
  }

  emitShowInstituteListViewEvent() {
    this.tempBreadcrumbLinkName = '';
    this.inAppDataTransferService.showInstituteListView(true);
  }

  tempBreadCrumbNameExists() {
    if (this.tempBreadcrumbLinkName) {
      return true;
    } else {
      return false;
    }
  }

  ngOnDestroy(): void {
    if (this.showTempNamesSubscription) {
      this.showTempNamesSubscription.unsubscribe();
    }
  }
}
