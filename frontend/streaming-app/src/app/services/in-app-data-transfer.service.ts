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
  private activeSideNavView = new Subject<String>();
  activeSideNavView$ = this.activeSideNavView.asObservable();

  // For updating status in case license is purchased
  private teacherFullInstituteView = new Subject<void>();
  teacherFullInstituteView$ = this.teacherFullInstituteView.asObservable();

  // For showing or hiding close button in preview course navbar
  private showPreviewCourseCloseButton = new Subject<boolean>();
  showPreviewCourseCloseButton$ = this.showPreviewCourseCloseButton.asObservable();

  private closePreviewCourseContentStatus = new Subject<void>();
  closePreviewCourseContent$ = this.closePreviewCourseContentStatus.asObservable();

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
  showTeacherFullInstituteView() {
    this.teacherFullInstituteView.next();
  }

  // Sends signal to show or hide close button
  showOrHideCloseButtonInCoursePreview(status: boolean) {
    this.showPreviewCourseCloseButton.next(status);
  }

  closePreviewCourseContent() {
    this.closePreviewCourseContentStatus.next();
  }
}
