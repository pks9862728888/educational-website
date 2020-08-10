import { webAppName } from './../../constants';
import { InAppDataTransferService } from '../services/in-app-data-transfer.service';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-teacher-workspace',
  templateUrl: './teacher-workspace.component.html',
  styleUrls: ['./teacher-workspace.component.css']
})
export class TeacherWorkspaceComponent implements OnInit, OnDestroy {

  // For showing sidenav toolbar
  mq: MediaQueryList;
  title = webAppName;
  opened: boolean;
  activeLink: string;
  showTempNamesSubscription: Subscription;
  tempBreadcrumbLinkName: string;
  routerActiveLinkSubscription: Subscription;

  constructor( private router: Router,
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
        } else if (val.url.includes('chatrooms')) {
          this.activeLink = 'CHATROOMS';
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
