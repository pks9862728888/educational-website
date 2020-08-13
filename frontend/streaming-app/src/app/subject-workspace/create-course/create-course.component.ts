import { HttpEventType } from '@angular/common/http';
import { Subscription, Subject } from 'rxjs';
import { UiService } from 'src/app/services/ui.service';
import { currentSubjectSlug, STUDY_MATERIAL_CONTENT_TYPE, STUDY_MATERIAL_VIEW, STUDY_MATERIAL_VIEW_REVERSE, STUDY_MATERIAL_CONTENT_TYPE_REVERSE } from './../../../constants';
import { InstituteApiService } from './../../services/institute-api.service';
import { Router } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { SubjectCourseMinDetails, StorageStatistics, SubjectCourseViewDetails, StudyMaterialDetails } from '../../models/subject.model';

@Component({
  selector: 'app-create-course',
  templateUrl: './create-course.component.html',
  styleUrls: ['./create-course.component.css']
})
export class CreateCourseComponent implements OnInit {

  mq: MediaQueryList;
  currentSubjectSlug: string;
  showGuidelines: boolean;
  openedPanelStep: number;
  selectedSidenav = 'UPLOAD_VIDEO';
  uploadError: string;
  addFilesDialog = false;
  showLoadingIndicator: boolean;
  loadingText = 'Loading Course Details...';
  showContentLoadingIndicator: boolean;
  loadingContentText = 'Fetching Content...';
  showReload: boolean;
  reloadText = 'Unable to load course details.';
  errorText: string;            // For showing fetching data error
  contentSuccessText: string;   // For showing upload success
  actionSuccessText: string;    // For showing reorder, shuffle, edit success
  contentError: string;         // For showing upload error
  contentReload: boolean;
  contentReloadText = 'Unable to load content.';
  viewOrder = ['MI', 'CO'];
  actionControlDialogDataSubscription: Subscription;
  allowTargetDateSetting = true;
  uploadingEvent = new Subject<String>();
  hideCloseContentLoadingErrorButton = true;
  deleteDialogDataSubscription: Subscription;

  // Data
  storage: StorageStatistics;
  courseDetailsMinStat: SubjectCourseViewDetails;
  viewData = {
    MI: [],
    CO: []
  };
  actionContent: StudyMaterialDetails;
  actionView: string;

  constructor(
    private media: MediaMatcher,
    private router: Router,
    private instituteApiService: InstituteApiService,
    private uiService: UiService
  ) {
    this.mq = media.matchMedia('(max-width: 600px)');
    this.currentSubjectSlug = sessionStorage.getItem(currentSubjectSlug);
    this.openedPanelStep = 0;
  }


  ngOnInit(): void {
    this.getMinCourseDetails();
  }

  getMinCourseDetails() {
    this.showLoadingIndicator = true;
    this.hideCloseContentLoadingErrorButton = true;
    this.showReload = false;
    this.errorText = null;
    this.instituteApiService.getMinCourseDetails(this.currentSubjectSlug).subscribe(
      ( result: SubjectCourseMinDetails ) => {
        this.showLoadingIndicator = false;
        this.storage = {
          'storage_used': result.storage_used,
          'total_storage': result.total_storage
        }
        this.courseDetailsMinStat = {
          'CO': result.CO,
          'MI': result.MI
        };
      },
      errors => {
        this.showLoadingIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.errorText = errors.error.error;
          } else {
            this.showReload = true;
          }
        } else {
          this.showReload = true;
        }
      }
    )
  }

  setOpenedPanelStep(step: number) {
    this.openedPanelStep = step;
    this.selectedSidenav = 'UPLOAD_VIDEO';
    this.addFilesDialog = false;

    // Get content if view does not have any content
    if (!this.hasContent(this.viewOrder[step])) {
      this.getContentOfView();
    }
  }

  getContentOfView() {
    this.showContentLoadingIndicator = true;
    this.contentError = null;
    this.contentReload = false;
    this.instituteApiService.getCourseContentOfSpecificView(
      this.currentSubjectSlug,
      this.viewOrder[this.openedPanelStep])
      .subscribe(
        (result: StudyMaterialDetails[] ) => {
          this.showContentLoadingIndicator = false;
          for(const content of result) {
            this.viewData[this.viewOrder[this.openedPanelStep]].push(content);
          }
          console.log(this.viewData);
        },
        errors => {
          this.showContentLoadingIndicator = false;
          console.log(errors);
          if (errors.errors) {
            if (errors.errors.error) {
              this.contentError = errors.error.error;
            } else {
              this.contentReload = true;
            }
          } else {
            this.contentReload = true;
          }
        }
      )
  }

  guidelineClicked() {
    this.showGuidelines = !this.showGuidelines;
  }

  editClicked() {

  }

  deleteClicked(content: StudyMaterialDetails) {
    this.actionContent = content;
    this.actionView = this.viewOrder[this.openedPanelStep];
    this.actionSuccessText = null;
    this.contentError = null;
    this.deleteDialogDataSubscription = this.uiService.dialogData$.subscribe(
      result => {
        if (result) {
          this.instituteApiService.deleteClassCourseContent(content.id.toString()).subscribe(
            () => {
              this.actionSuccessText = 'Delete successful.';
              this.hideCloseContentLoadingErrorButton = false;
              this.viewData[this.actionView].splice(this.actionContent, 1);
              this.courseDetailsMinStat[this.actionView] = Math.max(0, this.courseDetailsMinStat[this.actionView] - 1);
              if (this.actionContent.data.size) {
                this.storage.storage_used = Math.max(0, this.storage.storage_used - this.actionContent.data.size);
              }
              this.actionView = null;
              this.actionContent = null;
            },
            errors => {
              this.actionView = null;
              this.actionContent = null;
              if (errors.error) {
                if (errors.error.error) {
                  this.contentError = errors.error.error;
                } else {
                  this.contentError = 'Unable to delete at the moment. Please try again later.';
                }
              } else {
                this.contentError = 'Unable to delete at the moment. Please try again later.';
              }
            }
          );
        }
        this.unsubscribeDeleteDialogData();
      }
    );
    this.uiService.openDialog(
      'Are you sure you want to delete \"' + content.title + "\"?",
      'No',
      'Yes'
    );
  }

  unsubscribeDeleteDialogData() {
    if (this.deleteDialogDataSubscription) {
      this.deleteDialogDataSubscription.unsubscribe();
    }
  }

  reorderClicked() {

  }

  // For mobile view
  showActionsClicked(content: StudyMaterialDetails) {
    this.actionContent = content;
    this.actionControlDialogDataSubscription = this.uiService.actionControlDialogData$.subscribe(
      data => {
        if (data == 'EDIT') {
          this.editClicked();
        } else if (data == 'DELETE') {
          this.deleteClicked(this.actionContent);
        } else if (data == 'REORDER') {
          this.reorderClicked();
        }
        this.destroyActionControlDialogDataSubscription();
      }
    )
    this.uiService.openReorderEditDeleteDialog();
  }

  destroyActionControlDialogDataSubscription() {
    if (this.actionControlDialogDataSubscription) {
      this.actionControlDialogDataSubscription.unsubscribe();
    }
  }

  setActiveSidenav(text: string) {
    this.selectedSidenav = text;
  }

  uploadVideo(data: any) {

  }

  uploadImage(data: any) {
    data['view'] = this.viewOrder[this.openedPanelStep];
    console.log(data);
    this.instituteApiService.uploadStudyMaterial(this.currentSubjectSlug, data).subscribe(
      result => {
        if (result.type === HttpEventType.UploadProgress) {
          const percentDone = Math.round(100 * result.loaded / result.total);
          console.log('Progress ' + percentDone + '%');
        } else if (result.type === HttpEventType.Response) {
          console.log(result);
        }
      },
      errors => {
        console.log(errors);
      }
    )
  }

  uploadPdf(data: any) {

  }

  uploadExternalLink(data: any) {
    data['view'] = this.viewOrder[this.openedPanelStep];
    this.uploadingEvent.next('DISABLE');
    this.uploadError = null;
    this.contentSuccessText = null;
    this.instituteApiService.addSubjectExternalLinkCourseContent(
      this.currentSubjectSlug, data).subscribe(
        (result: StudyMaterialDetails) => {
          this.uploadingEvent.next('RESET');
          this.contentSuccessText = 'Uploaded Successfully.';
          this.viewData[this.viewOrder[this.openedPanelStep]].push(result);
          console.log(this.viewData[this.viewOrder[this.openedPanelStep]]);
        },
        errors => {
          this.uploadingEvent.next('ENABLE');
          if(errors.error) {
            if (errors.error.error) {
              this.uploadError = errors.error.error;
            } else {
              this.uploadError = 'Unable to upload. Please try again.';
            }
          } else {
            this.uploadError = 'Unable to upload. Please try again.';
          }
        }
      )
  }

  uploadFormError_(data: string) {
    this.uploadError = data;
  }

  closeUploadError() {
    this.uploadError = null;
  }

  toggleMeetInstructorFileUploadDialog() {
      this.addFilesDialog = !this.addFilesDialog;
  }

  contentClicked() {
    console.log('clicked');
  }

  closeErrorText() {
    this.errorText = null;
  }

  getViewName(key: string) {
    return STUDY_MATERIAL_VIEW[key];
  }

  getStudyMaterialCount(view: string) {
    return this.courseDetailsMinStat[view];
  }

  getStoragePercentFilled() {
    return 100 * this.storage.storage_used / this.storage.total_storage;
  }

  closeUploadSuccess() {
    this.contentSuccessText = null;
  }

  hasContent(view: string) {
    if (this.viewData[view].length > 0) {
      return true;
    } else {
      return false;
    }
  }

  isContentTypeImage(key: string) {
    if (key === STUDY_MATERIAL_CONTENT_TYPE_REVERSE['IMAGE']) {
      return true;
    } else {
      return false;
    }
  }

  isContentTypePdf(key: string) {
    if (key === STUDY_MATERIAL_CONTENT_TYPE_REVERSE['PDF']) {
      return true;
    } else {
      return false;
    }
  }

  isContentTypeVideo(key: string) {
    if (key === STUDY_MATERIAL_CONTENT_TYPE_REVERSE['VIDEO']) {
      return true;
    } else {
      return false;
    }
  }

  isContentTypeLink(key: string) {
    if (key === STUDY_MATERIAL_CONTENT_TYPE_REVERSE['EXTERNAL_LINK']) {
      return true;
    } else {
      return false;
    }
  }

  closeActionSuccess() {
    this.actionSuccessText = null;
  }

}
