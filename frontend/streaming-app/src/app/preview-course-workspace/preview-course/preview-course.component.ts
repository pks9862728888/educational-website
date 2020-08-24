import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { isContentTypeImage, isContentTypeVideo, isContentTypePdf, isContentTypeExternalLink } from '../../shared/utilityFunctions'

@Component({
  selector: 'app-preview-course',
  templateUrl: './preview-course.component.html',
  styleUrls: ['./preview-course.component.css']
})
export class PreviewCourseComponent implements OnInit {

  mq: MediaQueryList;
  openedPanelStep: number;
  openedWeekStep: number;
  isContentTypeImage = isContentTypeImage;
  isContentTypeVideo = isContentTypeVideo;
  isContentTypePdf = isContentTypePdf;
  isContentTypeLink = isContentTypeExternalLink;

  loadingIndicator: boolean;
  reloadIndicator: boolean;
  errorLoading: string;


  constructor(
    private media: MediaMatcher
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.openedPanelStep = 0;
  }

  ngOnInit(): void {
  }

  loadMinPreviewDetails() {
    alert('Here');
  }

  setOpenedPanelStep(step: number) {
    if (this.openedPanelStep === step) {
      this.openedPanelStep = null;
    } else {
      this.openedPanelStep = step;
    }
    this.openedWeekStep = null;
  }

  setOpenedWeekStep(step: number) {
    if (this.openedWeekStep === step) {
      this.openedWeekStep = null;
    } else {
      this.openedWeekStep = step;
    }
  }

}
