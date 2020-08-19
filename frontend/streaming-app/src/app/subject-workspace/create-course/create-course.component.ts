import { ViewDetails } from './../../models/subject.model';
import { HttpEventType } from '@angular/common/http';
import { Subscription, Subject } from 'rxjs';
import { UiService } from 'src/app/services/ui.service';
import { currentSubjectSlug, STUDY_MATERIAL_CONTENT_TYPE, STUDY_MATERIAL_VIEW, STUDY_MATERIAL_VIEW_REVERSE, STUDY_MATERIAL_CONTENT_TYPE_REVERSE, actionContent, activeCreateCourseView } from './../../../constants';
import { InstituteApiService } from './../../services/institute-api.service';
import { Router } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { SubjectCourseMinDetails, StorageStatistics, SubjectCourseViewDetails, StudyMaterialDetails } from '../../models/subject.model';
import { WeekDay } from '@angular/common';

@Component({
  selector: 'app-create-course',
  templateUrl: './create-course.component.html',
  styleUrls: ['./create-course.component.css']
})
export class CreateCourseComponent implements OnInit, OnDestroy {

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
  actionControlDialogDataSubscription: Subscription;
  allowTargetDateSetting = true;
  uploadingEvent = new Subject<String>();
  hideCloseContentLoadingErrorButton = true;
  deleteDialogDataSubscription: Subscription;
  uploadProgressEvent = new Subject<{loaded: number, total: number}>();

  showView: string;

  // Data
  storage: StorageStatistics;
  viewDetails: ViewDetails;
  viewOrder: Array<string>;
  viewData = {};
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
    this.showView = sessionStorage.getItem(activeCreateCourseView);
    if (!this.showView) {
      this.showView = 'CREATE';
    }
  }


  ngOnInit(): void {
    this.getMinCourseDetails();
    this.openedPanelStep = 0;
  }

  getMinCourseDetails() {
    this.showLoadingIndicator = true;
    this.hideCloseContentLoadingErrorButton = true;
    this.showReload = false;
    this.errorText = null;
    this.instituteApiService.getMinCourseDetails(this.currentSubjectSlug).subscribe(
      (result: SubjectCourseMinDetails) => {
        console.log(result)
        this.showLoadingIndicator = false;
        this.storage = result.storage;
        this.viewOrder = result.view_order;
        this.viewDetails = result.view_details;

        for(let view of this.viewOrder) {
          if (view === 'MI' || view === 'CO') {
            this.viewData[view] = [];
          } else {
            this.viewData[view] = {};
          }
        }
        console.log(this.viewData);
        console.log(this.storage);
        console.log(this.viewOrder)
        console.log(this.viewDetails);
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
    // if (!this.hasContent(this.viewOrder[step])) {
    //   this.getContentOfView();
    // }
    this.getContentOfView();
  }

  getContentOfView() {
    this.showContentLoadingIndicator = true;
    this.contentError = null;
    this.contentReload = false;
    const view = this.viewOrder[this.openedPanelStep];
    this.instituteApiService.getCourseContentOfSpecificView(
      this.currentSubjectSlug,
      view)
      .subscribe(
        (result: StudyMaterialDetails[] ) => {
          console.log(result);
          this.showContentLoadingIndicator = false;
          this.viewData[view] = result;
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

  editClicked() {}

  deleteClicked(content: StudyMaterialDetails) {
    const actionContent = content;
    const actionView = this.viewOrder[this.openedPanelStep];
    this.actionSuccessText = null;
    this.contentError = null;
    this.deleteDialogDataSubscription = this.uiService.dialogData$.subscribe(
      result => {
        if (result) {
          this.instituteApiService.deleteClassCourseContent(content.id.toString()).subscribe(
            () => {
              this.actionSuccessText = 'Delete successful.';
              this.hideCloseContentLoadingErrorButton = false;
              if (actionContent.week) {
                this.viewData[actionView][actionContent.week].splice(
                  this.findIdInArray(this.viewData[actionView][actionContent.week], actionContent.id), 1);
                this.viewDetails[actionContent.view][actionContent.week] -= 1;
              } else {
                this.viewData[actionView].splice(this.viewData[actionView].indexOf(actionContent), 1);
              }
              this.viewDetails[actionContent.view]['count'] -= 1;
              if (actionContent.data.size) {
                this.storage.storage_used = Math.max(0, this.storage.storage_used - actionContent.data.size);
              }
            },
            errors => {
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

  reorderClicked() {}

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

  uploadMediaFile(data: any) {
    data['view_key'] = this.viewOrder[this.openedPanelStep];
    this.uploadError = null;
    this.contentSuccessText = null;
    this.uploadingEvent.next('DISABLE');
    this.uploadProgressEvent.next({
      'total': data.size,
      'loaded': 0,
    });
    console.log(data);
    this.instituteApiService.uploadStudyMaterial(this.currentSubjectSlug, data).subscribe(
      result => {
        if (result.type === HttpEventType.UploadProgress) {
          this.uploadProgressEvent.next({
            'total': result.total,
            'loaded': result.loaded,
          });
        } else if (result.type === HttpEventType.Response) {
          this.uploadingEvent.next('RESET');
          this.contentSuccessText = 'Upload successful.';
          if (!result['week']) {
            this.viewData[result.body['view']].push(result.body);
          } else {
            this.viewData[result.body['view']][result.body['week']].push(result.body);
            this.viewDetails[data['view_key']][result.body['week']] += 1;
          }
          this.storage.storage_used += result.body['data']['size'];
          this.viewDetails[data['view_key']].count += 1;
        }
      },
      errors => {
        this.uploadingEvent.next('ENABLE');
        if (errors.error) {
          if (errors.error.error) {
            this.uploadError = errors.error.error;
          } else {
            this.uploadError = 'Upload failed.';
          }
        } else {
          this.uploadError = 'Upload failed.';
        }
      }
    )
  }

  uploadExternalLink(data: any) {
    data['view_key'] = this.viewOrder[this.openedPanelStep];
    this.uploadingEvent.next('DISABLE');
    this.uploadError = null;
    this.contentSuccessText = null;
    this.instituteApiService.addSubjectExternalLinkCourseContent(
      this.currentSubjectSlug, data).subscribe(
        (result: StudyMaterialDetails) => {
          console.log(result);
          this.uploadingEvent.next('RESET');
          this.contentSuccessText = 'Uploaded Successfully.';
          if (!result['week']) {
            this.viewData[result.view].push(result);
          } else {
            this.viewData[result.view][result.week].push(result);
            this.viewDetails[data['view_key']][result['week']] += 1;
          }
          this.viewDetails[data['view_key']].count += 1;
          console.log(this.viewDetails);
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
      this.contentSuccessText = null;
      this.uploadError = null;
  }

  contentClicked(content: StudyMaterialDetails) {
    if (content.content_type === STUDY_MATERIAL_CONTENT_TYPE_REVERSE['EXTERNAL_LINK']) {
      window.open('//' + content.data.url, '_blank');
    } else if (content.content_type === STUDY_MATERIAL_CONTENT_TYPE_REVERSE['IMAGE']) {
      this.showView = 'VIEW_IMAGE';
      sessionStorage.setItem(activeCreateCourseView, 'VIEW_IMAGE');
      sessionStorage.setItem(actionContent, JSON.stringify(content));
    } else if (content.content_type === STUDY_MATERIAL_CONTENT_TYPE_REVERSE['VIDEO']) {
      this.showView = 'VIEW_VIDEO';
      sessionStorage.setItem(activeCreateCourseView, 'VIEW_VIDEO');
      sessionStorage.setItem(actionContent, JSON.stringify(content));
    } else if (content.content_type === STUDY_MATERIAL_CONTENT_TYPE_REVERSE['PDF']) {
      this.showView = 'VIEW_PDF';
      sessionStorage.setItem(activeCreateCourseView, 'VIEW_PDF');
      sessionStorage.setItem(actionContent, JSON.stringify(content));
    }
  }

  findIdInArray(array, id) {
    for(let idx in array) {
      const arr = array[idx]
      if (arr['id'] === id) {
        return idx;
      }
    }
    return -1;
  }

  showCreateView(event: any) {
    if (event === 'DELETED') {
      const content: StudyMaterialDetails = JSON.parse(sessionStorage.getItem(actionContent));
      this.viewData[content.view].splice(
        this.findIdInArray(this.viewData[content.view], content.id), 1
      );
      this.actionSuccessText = 'Delete successful.';
    } else if (event) {
      this.viewData[event.view].splice(
        this.findIdInArray(this.viewData[event.view], event.id),
        1,
        event
      );
    }
    this.showView = 'CREATE';
    sessionStorage.removeItem(actionContent);
    sessionStorage.removeItem(activeCreateCourseView);
  }

  closeErrorText() {
    this.errorText = null;
  }

  getViewName(key: string) {
    return this.viewDetails[key]['name'];
  }

  getStudyMaterialCount(view: string) {
    return this.viewDetails[view]['count'];
  }

  getStoragePercentFilled() {
    return (100 * this.storage.storage_used / this.storage.total_storage).toFixed(3);
  }

  closeUploadSuccess() {
    this.contentSuccessText = null;
  }

  hasContent(view: string) {
    if (view === 'MI' || view === 'CO') {
      if (this.viewData[view].length > 0) {
        return true;
      } else {
        return false;
      }
    } else {
      // if (this.viewData[view][week].length > 0) {
      //   return true;
      // } else {
      //   return false;
      // }
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

  ngOnDestroy() {
    sessionStorage.removeItem(actionContent);
    sessionStorage.removeItem(activeCreateCourseView);
  }

}
