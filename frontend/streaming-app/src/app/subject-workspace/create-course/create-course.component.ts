import { WindowRefService } from './../../services/window-ref.service';
import { Router } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-create-course',
  templateUrl: './create-course.component.html',
  styleUrls: ['./create-course.component.css']
})
export class CreateCourseComponent implements OnInit {

  mq: MediaQueryList;
  showGuidelines: boolean;
  openedPanelStep = 0;
  selectedSidenav = 'UPLOAD_VIDEO';
  showData: any;
  uploadFormError: string;
  addFilesDialog = false;

  constructor(
    private media: MediaMatcher,
    private router: Router
  ) {
    this.mq = media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
  }

  guidelineClicked() {
    this.showGuidelines = !this.showGuidelines;
  }

  setOpenedPanelStep(step: number) {
    this.openedPanelStep = step;
    this.selectedSidenav = 'UPLOAD_VIDEO';
  }

  setActiveSidenav(text: string) {
    this.selectedSidenav = text;
  }

  uploadVideo(data: any) {
    this.showData = data;
  }

  uploadImage(data: any) {
    this.showData = data;
  }

  uploadPdf(data: any) {
    this.showData = data;
  }

  uploadExternalLink(data: any) {
    this.showData = data;
  }

  uploadFormError_(data: string) {
    this.uploadFormError = data;
  }

  closeFileTypeError() {
    this.uploadFormError = null;
  }

  toggleMeetInstructorFileUploadDialog() {
      this.addFilesDialog = !this.addFilesDialog;
  }

  contentClicked() {
    console.log('clicked');
  }

}
