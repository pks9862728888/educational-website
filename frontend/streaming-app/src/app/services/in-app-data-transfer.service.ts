import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InAppDataTransferService {

  // Creating observable to display links in breadcrumb
  private activeBreadcrumbLinkData = new Subject<string>();
  activeBreadcrumbLinkData$ = this.activeBreadcrumbLinkData.asObservable();

  // Creating observable to navigate to institutes view
  private setInstituteViewActive = new Subject<boolean>();
  setInstituteViewActive$ = this.setInstituteViewActive.asObservable();

  // Creating observable for selecting the active link in sidenav
  private activeSideNavView = new Subject<string>();
  activeSideNavView$ = this.activeSideNavView.asObservable();

  // For updating status in case license is purchased
  private teacherLmsCmsView = new Subject<void>();
  teacherLmsCmsView$ = this.teacherLmsCmsView.asObservable();

  // For showing or hiding close button in preview course navbar
  private showPreviewCourseCloseButton = new Subject<boolean>();
  showPreviewCourseCloseButton$ = this.showPreviewCourseCloseButton.asObservable();

  private closePreviewCourseContentStatus = new Subject<void>();
  closePreviewCourseContent$ = this.closePreviewCourseContentStatus.asObservable();

  // For sending profile picture updated data
  private profilePictureUpdatedData = new Subject();
  profilePictureUpdatedData$ = this.profilePictureUpdatedData.asObservable();

  constructor() { }

  // Sends active breadcrumb sublink text
  sendActiveBreadcrumbLinkData(data: string) {
    this.activeBreadcrumbLinkData.next(data);
  }

  // Sends status symbol to show institute view
  showInstituteListView(status: boolean) {
    this.setInstituteViewActive.next(status);
  }

  // Sends the active link to sidenav
  setSidenavActiveLink(link: string) {
    this.activeSideNavView.next(link);
  }

  // Sends status to show full institute view
  showTeacherLmsCmsInstituteView() {
    this.teacherLmsCmsView.next();
  }

  // Sends signal to show or hide close button
  showOrHideCloseButtonInCoursePreview(status: boolean) {
    this.showPreviewCourseCloseButton.next(status);
  }

  closePreviewCourseContent() {
    this.closePreviewCourseContentStatus.next();
  }

  sendProfilePictureUpdatedData(data: any) {
    this.profilePictureUpdatedData.next(data);
  }
}
