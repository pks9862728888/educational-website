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
}
