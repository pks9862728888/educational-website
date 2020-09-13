import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-create-new-course',
  templateUrl: './create-new-course.component.html',
  styleUrls: ['./create-new-course.component.css']
})
export class CreateNewCourseComponent implements OnInit {

  mq: MediaQueryList;
  errorText: string;
  showLoadingIndicator: boolean;
  showReload: boolean;
  hasSubjectPerm: boolean;
  selectedLecture: any;

  openedPanelStep: number;
  editContentError: boolean;

  editContentFormEvent = new Subject<string>();

  viewOrder = ['MI', 'CO', 'SDF'];

  constructor(
    private media: MediaMatcher
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.openedPanelStep = 0;
    this.hasSubjectPerm = true;
  }

  ngOnInit(): void {
  }

  getMinCourseDetails() {

  }

  editClicked() {

  }

  deleteClicked() {

  }

  showActionsClicked() {

  }

  updateContent(content) {

  }

  closeEditForm(content) {

  }

  openLecture() {
    this.selectedLecture = 'sdfs';
  }

  closeLecture() {
    this.selectedLecture = null;
  }

  setOpenedPanelStep(step: number) {
    if (this.openedPanelStep === step) {
      this.openedPanelStep = null;
    } else {
      this.openedPanelStep = step;
    }
  }

  closeErrorText() {
    this.errorText = null;
  }

  closeEditContentError() {
    this.editContentError = null;
  }

}
