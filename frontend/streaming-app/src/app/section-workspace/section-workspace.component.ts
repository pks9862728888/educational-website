import { currentSectionSlug, INSTITUTE_TYPE_REVERSE, currentClassSlug, webAppName } from './../../constants';
import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { Router, NavigationEnd } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { InAppDataTransferService } from '../services/in-app-data-transfer.service';
import { currentInstituteSlug, currentInstituteType } from '../../constants';

@Component({
  selector: 'app-section-workspace',
  templateUrl: './section-workspace.component.html',
  styleUrls: ['./section-workspace.component.css']
})
export class SectionWorkspaceComponent implements OnInit {

  mq: MediaQueryList;
  webAppName = webAppName;
  currentInstituteSlug: string;
  currentSectionSlug: string;
  currentInstituteType: string;
  baseUrl: string;
  opened: boolean;
  activeLink: string;
  navbarActiveLinkSubscription: Subscription;
  showTempNamesSubscription: Subscription;
  tempBreadcrumbLinkName: string;
  routerEventsSubscription: Subscription;

  constructor(
    private router: Router,
    private media: MediaMatcher,
    private inAppDataTransferService: InAppDataTransferService) {

    this.mq = this.media.matchMedia('(max-width: 768px)');
    this.activeLink = 'SECTION_PERMISSIONS';
    this.routerEventsSubscription = router.events.subscribe(val => {
      if (val instanceof NavigationEnd) {
        if (val.url.includes('permissions')) {
          this.activeLink = 'SECTION_PERMISSIONS';
        }
      }
    });
    this.currentSectionSlug = sessionStorage.getItem(currentSectionSlug);
    this.baseUrl = '/section-workspace/' + this.currentSectionSlug.slice(0, -10);
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
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.currentInstituteType = sessionStorage.getItem(currentInstituteType);
  }

  navigateToAppropriateInstituteWorkspace(path: string) {
    if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE.School) {
      this.router.navigate(['/school-workspace/' + this.currentInstituteSlug + path]);
    } else if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE.Coaching) {
      this.router.navigate(['/coaching-workspace/' + this.currentInstituteSlug + path]);
    } else if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE.College) {
      this.router.navigate(['/college-workspace/' + this.currentInstituteSlug + path]);
    }
  }

  navigate(link: string) {
    if (this.mq.matches === true) {
      this.opened = false;
    }
    if (link !== this.activeLink) {
      if (link === 'HOME') {
        this.router.navigate(['/home']);
      } else if (link === 'CLASS_SECTIONS') {
        this.router.navigate(['/class-workspace/' + sessionStorage.getItem(currentClassSlug).slice(0, -10) + '/sections']);
      } else if (link === 'CURRENT_INSTITUTE') {
        this.navigateToAppropriateInstituteWorkspace('/profile');
      } else if (link === 'INSTITUTES') {
        this.router.navigate(['/teacher-workspace/institutes']);
      } else {
        if (link === 'SECTION_PERMISSIONS') {
          this.router.navigate([this.baseUrl + '/permissions']);
        }
      }
    }
  }

  tempBreadCrumbNameExists() {
    if (this.tempBreadcrumbLinkName) {
      return true;
    } else {
      return false;
    }
  }

  ngOnDestroy(): void {
    if (this.routerEventsSubscription) {
      this.routerEventsSubscription.unsubscribe();
    }
    if (this.showTempNamesSubscription) {
      this.showTempNamesSubscription.unsubscribe();
    }
  }
}
