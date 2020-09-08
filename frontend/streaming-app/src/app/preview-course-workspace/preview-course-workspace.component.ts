import { InstituteApiService } from 'src/app/services/institute-api.service';
import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { webAppName, currentInstituteSlug, currentSubjectSlug, currentInstituteType, INSTITUTE_TYPE_REVERSE, currentClassSlug, previewActionContent, is_teacher, is_student } from '../../constants';
import { Subscription } from 'rxjs';
import { InAppDataTransferService } from '../services/in-app-data-transfer.service';
import { MediaMatcher } from '@angular/cdk/layout';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-preview-course-workspace',
  templateUrl: './preview-course-workspace.component.html',
  styleUrls: ['./preview-course-workspace.component.css']
})
export class PreviewCourseWorkspaceComponent implements OnInit {

  mq: MediaQueryList;
  title = webAppName;
  currentInstituteSlug: string;
  currentSubjectSlug: string;
  currentInstituteType: string;
  userType: string;
  baseUrl: string;
  opened: boolean;
  activeLink: string;
  tempBreadcrumbLinkName: string;
  routerEventsSubscription: Subscription;
  showCloseIcon: boolean;
  showOrHideCloseButtonSubscription: Subscription;

  constructor(
    private router: Router,
    private media: MediaMatcher,
    private inAppDataTransferService: InAppDataTransferService,
    private chageDetectorRef: ChangeDetectorRef
    ) {
    this.mq = this.media.matchMedia('(max-width: 768px)');
    this.activeLink = 'COURSE_PREVIEW';
    this.routerEventsSubscription = router.events.subscribe(val => {
      if (val instanceof NavigationEnd) {
        if (val.url.includes('view-peers')) {
          this.activeLink = 'VIEW_PEERS';
        } else if (val.url.includes('join-groups')) {
          this.activeLink = 'JOIN_GROUPS';
        } else if (val.url.includes('announcements')) {
          this.activeLink = 'ANNOUNCEMENTS';
        } else if(val.url.includes('preview')) {
          this.activeLink = 'COURSE_PREVIEW';
        }
      }
    });
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.currentSubjectSlug = sessionStorage.getItem(currentSubjectSlug);
    this.baseUrl = '/preview-course-workspace/' + this.currentSubjectSlug.slice(0, -10);
    this.currentInstituteType = sessionStorage.getItem(currentInstituteType);
    this.showOrHideCloseButtonSubscription = this.inAppDataTransferService.showPreviewCourseCloseButton$.subscribe(
      (status: boolean) => {
        this.showCloseIcon = status;
        this.chageDetectorRef.detectChanges();
      }
    );
    if (sessionStorage.getItem(is_teacher) === 'true') {
      this.userType = 'TEACHER';
    } else {
      this.userType = 'STUDENT';
    }
  }

  ngOnInit(): void {
    // For keeping the sidenav opened in desktop view in the beginning
    if (this.mq.matches === true) {
      this.opened = false;
    } else {
      this.opened = true;
    }
  }

  navigate(link: string) {
    if (this.mq.matches === true) {
      this.opened = false;
    }
    if (link !== this.activeLink) {
        if (link === 'COURSE_PREVIEW') {
          this.router.navigate([this.baseUrl + '/preview']);
        } else if (link === 'VIEW_PEERS') {
          this.router.navigate([this.baseUrl + '/view-peers']);
        } else if (link === 'JOIN_GROUPS') {
          this.router.navigate([this.baseUrl + '/join-groups']);
        } else if (link === 'ANNOUNCEMENTS') {
          this.router.navigate([this.baseUrl + '/announcements']);
        } else if (link === 'EXIT_COURSE') {
          if (sessionStorage.getItem(is_student)) {
            const workspaceBaseUrl = this.getInstituteWorkspaceType();
            this.router.navigate([workspaceBaseUrl + this.currentInstituteSlug + '/student-courses']);
          } else if (sessionStorage.getItem(is_teacher)) {
            this.router.navigate(['subject-workspace/' + this.currentInstituteSlug + '/create-course']);
          }
        }
    }
  }

  getInstituteWorkspaceType() {
    const currentInstituteType_ = sessionStorage.getItem(currentInstituteType);
    if (currentInstituteType_ === INSTITUTE_TYPE_REVERSE['School']) {
      return 'school-workspace/';
    } else if (currentInstituteType_ === INSTITUTE_TYPE_REVERSE['Coaching']) {
      return 'coaching-workspace/';
    } else if (currentInstituteType_ === INSTITUTE_TYPE_REVERSE['College']) {
      return 'college-workspace/';
    }
  }

  closePreviewClicked() {
    this.inAppDataTransferService.closePreviewCourseContent();
  }

  userIsTeacher() {
    if (sessionStorage.getItem(is_teacher) === 'true') {
      return true;
    } else {
      return false;
    }
  }

  ngOnDestroy(): void {
    if (this.routerEventsSubscription) {
      this.routerEventsSubscription.unsubscribe();
    }
    if (this.showOrHideCloseButtonSubscription) {
      this.showOrHideCloseButtonSubscription.unsubscribe();
    }
  }
}
