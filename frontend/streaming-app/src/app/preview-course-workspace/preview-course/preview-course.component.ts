import { currentInstituteSlug, currentSubjectSlug } from './../../../constants';
import { InstituteApiService } from './../../services/institute-api.service';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { isContentTypeImage, isContentTypeVideo, isContentTypePdf, isContentTypeExternalLink } from '../../shared/utilityFunctions'
import { SubjectPreviewCourseMinDetails } from '../../models/subject.model';

@Component({
  selector: 'app-preview-course',
  templateUrl: './preview-course.component.html',
  styleUrls: ['./preview-course.component.css']
})
export class PreviewCourseComponent implements OnInit {

  mq: MediaQueryList;
  currentSubjectSlug: string;
  currentInstituteSlug: string;
  openedPanelStep: number;
  openedWeekStep: number;
  isContentTypeImage = isContentTypeImage;
  isContentTypeVideo = isContentTypeVideo;
  isContentTypePdf = isContentTypePdf;
  isContentTypeLink = isContentTypeExternalLink;

  loadingIndicator: boolean;
  reloadIndicator: boolean;
  errorLoading: string;
  loadingContentIndicator: boolean;
  reloadContentIndicator: boolean;
  errorContentLoading: string;

  // Data
  viewOrder = []
  instructors = []
  viewDetails = {}


  constructor(
    private media: MediaMatcher,
    private instituteApiService: InstituteApiService
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.currentSubjectSlug = sessionStorage.getItem(currentSubjectSlug);
    this.openedPanelStep = 0;
  }

  ngOnInit(): void {
    this.loadMinPreviewDetails();
  }

  loadMinPreviewDetails() {
    this.loadingIndicator = true;
    this.reloadIndicator = false;
    this.errorLoading = null;
    this.instituteApiService.getMinSubjectCoursePreviewDetails(
      this.currentInstituteSlug,
      this.currentSubjectSlug
    ).subscribe(
      (result: SubjectPreviewCourseMinDetails) => {
        this.loadingIndicator = false;
        this.viewOrder = result.view_order;
        this.viewDetails = result.view_details;
        this.instructors = result.instructors;
        console.log(result);
      },
      errors => {
        this.loadingIndicator = false;
        if (errors.errors) {
          if (errors.error.error) {
            this.errorLoading = errors.error.error;
          } else {
            this.reloadIndicator = true;
          }
        } else {
          this.reloadIndicator = true;
        }
      }
    )
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

  loadViewData(view: string) {

  }

  getViewName(view: string) {
    return this.viewDetails[view].name;
  }

  getViewContentCount(view: string) {
    return this.viewDetails[view].count;
  }

  hasAssignedInstructors() {
    if (this.instructors.length > 0) {
      return true;
    } else {
      return false;
    }
  }

}
