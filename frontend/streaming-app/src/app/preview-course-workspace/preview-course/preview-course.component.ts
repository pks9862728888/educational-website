import { Subscription } from 'rxjs';
import { InAppDataTransferService } from './../../services/in-app-data-transfer.service';
import { Router } from '@angular/router';
import { currentInstituteSlug, currentSubjectSlug, STUDY_MATERIAL_CONTENT_TYPE_REVERSE, previewActionContent, selectedPreviewContentType } from './../../../constants';
import { InstituteApiService } from './../../services/institute-api.service';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { isContentTypeImage, isContentTypeVideo, isContentTypePdf, isContentTypeExternalLink } from '../../shared/utilityFunctions'
import { SubjectPreviewCourseMinDetails, StudyMaterialPreviewDetails } from '../../models/subject.model';


@Component({
  selector: 'app-preview-course',
  templateUrl: './preview-course.component.html',
  styleUrls: ['./preview-course.component.css']
})
export class PreviewCourseComponent implements OnInit, OnDestroy {

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

  showDetails = false;
  contentOpened: boolean;
  closePreviewCourseContentStatusSubscription: Subscription;
  activeAction = 'Q&A';

  // Data
  viewOrder = []
  instructors = []
  viewDetails = {}
  viewData = {}
  selectedContent: StudyMaterialPreviewDetails;


  constructor(
    private media: MediaMatcher,
    private instituteApiService: InstituteApiService,
    private inAppDataTransferService: InAppDataTransferService,
    private router: Router
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.currentSubjectSlug = sessionStorage.getItem(currentSubjectSlug);
    if (sessionStorage.getItem(previewActionContent)) {
      this.selectedContent = JSON.parse(sessionStorage.getItem(previewActionContent));
      this.contentOpened = true;
    }
  }

  ngOnInit(): void {
    this.loadMinPreviewDetails();
    if (this.selectedContent) {
      this.closePreviewCourseContentStatusSubscription = this.inAppDataTransferService.closePreviewCourseContent$.subscribe(
        () => {
          this.closePreviewClicked();
          this.closePreviewCourseContentStatusSubscription.unsubscribe();
        }
      );
      this.inAppDataTransferService.showOrHideCloseButtonInCoursePreview(true);
    }
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

        for (let view of this.viewOrder) {
          if (view === 'MI' || view === 'CO') {
            this.viewData[view] = [];
          } else {
            this.viewData[view] = {};
            for (let week of this.viewDetails[view]['weeks']) {
              this.viewData[view][week] = [];
            }
          }
        }
        console.log(this.viewData);
        console.log(this.viewDetails);
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
      this.loadViewData(this.viewOrder[this.openedPanelStep]);
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
    this.loadingContentIndicator = true;
    this.errorContentLoading = null;
    this.reloadContentIndicator = false;
    this.instituteApiService.getInstituteSpecificCourseContentPreview(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      view
    ).subscribe(
      (data: StudyMaterialPreviewDetails) => {
        this.loadingContentIndicator = false;
        this.viewData[view] = data;
        console.log(this.viewData);
      },
      errors => {
        this.loadingContentIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.errorContentLoading = errors.error.error;
          } else {
            this.reloadContentIndicator = true;
          }
        } else {
          this.reloadContentIndicator = true;
        }
      }
    )
  }

  contentClicked(content: StudyMaterialPreviewDetails) {
    if (content.content_type === STUDY_MATERIAL_CONTENT_TYPE_REVERSE['EXTERNAL_LINK']) {
      window.open('//' + content.data.url, '_blank');
    } else {
      sessionStorage.setItem(previewActionContent, JSON.stringify(content));
      this.selectedContent = content;
      this.inAppDataTransferService.showOrHideCloseButtonInCoursePreview(true);
      this.closePreviewCourseContentStatusSubscription = this.inAppDataTransferService.closePreviewCourseContent$.subscribe(
        () => {
          this.closePreviewClicked();
          this.inAppDataTransferService.showOrHideCloseButtonInCoursePreview(false);
          this.closePreviewCourseContentStatusSubscription.unsubscribe();
        }
      );
      this.contentOpened = true;
      sessionStorage.setItem(selectedPreviewContentType, content.content_type);
    }
  }

  closePreviewClicked() {
    this.contentOpened = false;
    this.selectedContent = null;
    this.activeAction = 'DESCRIPTION';
    sessionStorage.removeItem(previewActionContent);
    sessionStorage.removeItem(selectedPreviewContentType);
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

  viewHasContent(view: string) {
    if (view === 'MI' || view === 'CO') {
      if (this.viewData[view].length > 0) {
        return true;
      } else {
        return false;
      }
    } else {
      if (this.viewData[view][this.openedWeekStep].length > 0) {
        return true;
      } else {
        return false;
      }
    }
  }

  getDuration(duration: number) {
    let time = '';
    if (duration > 3600) {
      time = time + (duration / 3600).toString() + ' hour ';
      duration = duration % 3600;
    }
    if (duration > 60) {
      time = time + (duration / 60).toString() + ' minutes ';
      duration = duration % 60;
    }
    if (duration > 0) {
      time = time + duration.toString() + ' seconds';
    }
    return time;
  }

  toggleShowDetails() {
    this.showDetails = !this.showDetails;
  }

  actionClicked(actionType: string) {
    this.activeAction = actionType;
  }

  ngOnDestroy() {
    sessionStorage.removeItem(previewActionContent);
    this.inAppDataTransferService.closePreviewCourseContent();
  }

}
