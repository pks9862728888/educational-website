import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { webAppName } from '../../constants';
import { Subscription } from 'rxjs';
import { MediaMatcher } from '@angular/cdk/layout';
import { InAppDataTransferService } from '../services/in-app-data-transfer.service';

@Component({
  selector: 'app-student-workspace',
  templateUrl: './student-workspace.component.html',
  styleUrls: ['./student-workspace.component.css']
})
export class StudentWorkspaceComponent implements OnInit {

  mq: MediaQueryList;
  webAppName = webAppName;
  opened: boolean;
  activeLink: string;
  showTempNamesSubscription: Subscription;
  tempBreadcrumbLinkName: string;
  routerActiveLinkSubscription: Subscription;

  constructor(
    private router: Router,
    private media: MediaMatcher,
    private inAppDataTransferService: InAppDataTransferService ) {

    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.activeLink = 'PROFILE';
    this.routerActiveLinkSubscription = router.events.subscribe(val => {
      if (val instanceof NavigationEnd) {
        if (val.url.includes('profile')) {
          this.activeLink = 'PROFILE';
        } else if (val.url.includes('institutes')) {
          this.activeLink = 'INSTITUTES';
        } else if (val.url.includes('courses')) {
          this.activeLink = 'COURSES';
        }
      }
    });
  }

  ngOnInit(): void {
    // For keeping the sidenav opened in desktop view in the beginning
    if (this.mq.matches === true) {
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

  // For navigating to student-workspace view
  navigate(link: string) {
    if (link !== this.activeLink) {
      this.activeLink = link;

      if (this.activeLink === 'HOME') {
        this.router.navigate(['/home']);
      } else {
        this.router.navigate(['/student-workspace/' + link.toLowerCase()]);
      }
    }
  }

  // For navbar
  performAction(link: string) {
    // Hiding navbar if it is mobile
    if (this.mq.matches === true) {
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
    if (this.routerActiveLinkSubscription) {
      this.routerActiveLinkSubscription.unsubscribe();
    }
  }

}
