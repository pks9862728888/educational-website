import { FormGroup } from '@angular/forms';
import { Subscription, Subject } from 'rxjs';
import { UiService } from 'src/app/services/ui.service';
import { currentSubjectSlug, STUDY_MATERIAL_CONTENT_TYPE, STUDY_MATERIAL_VIEW, STUDY_MATERIAL_VIEW_REVERSE, STUDY_MATERIAL_CONTENT_TYPE_REVERSE, actionContent, activeCreateCourseView, currentInstituteSlug } from './../../../constants';
import { InstituteApiService } from './../../services/institute-api.service';
import { Router } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { SubjectCourseMinDetails, StorageStatistics, ViewDetails, SubjectCourseViewDetails, StudyMaterialDetails, CreateSubjectModuleResponse } from '../../models/subject.model';

@Component({
  selector: 'app-create-course',
  templateUrl: './create-course.component.html',
  styleUrls: ['./create-course.component.css']
})
export class CreateCourseComponent implements OnInit, OnDestroy {

  mq: MediaQueryList;
  currentSubjectSlug: string;
  currentInstituteSlug: string;
  showGuidelines: boolean;
  openedPanelStep: number;
  openedWeekStep: number;
  uploadError: string;
  addContentDialog = false;
  showLoadingIndicator: boolean;
  showContentLoadingIndicator: boolean;
  showReload: boolean;
  errorText: string;            // For showing fetching data error
  contentSuccessText: string;   // For showing upload success
  contentError: string;         // For showing upload error
  contentReload: boolean;
  actionControlDialogDataSubscription: Subscription;
  allowTargetDateSetting = true;
  hideCloseContentLoadingErrorButton = true;
  deleteDialogDataSubscription: Subscription;

  showAddWeekSpinner: boolean;
  showDeleteWeekSpinner: boolean;
  deleteWeekError: string;
  deleteWeekSubscription: Subscription;
  showDeleteModuleSpinner: boolean;
  editDeleteModuleError: string;
  deleteModuleSubscription: Subscription;

  showAddModuleForm = false;
  addModuleIndicator: boolean;
  addModuleFormEvent = new Subject<string>();
  createModuleButtonText: string;
  addModuleError: string;

  showEditModuleForm = false;
  editModuleIndicator: boolean;
  editModuleFormEvent = new Subject<string>();
  editModuleButtonText: string;
  selectedModuleName: string;
  // addModuleError: string;

  showView: string;
  activeView: string;

  // Data
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
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.currentSubjectSlug = sessionStorage.getItem(currentSubjectSlug);
    this.showView = sessionStorage.getItem(activeCreateCourseView);
    if (!this.showView) {
      this.showView = 'CREATE';
    }
  }

  ngOnInit(): void {
    this.getMinCourseDetails();
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    if (this.mq.matches) {
      this.createModuleButtonText = 'Create';
      this.editModuleButtonText = 'Update';
    } else {
      this.createModuleButtonText = 'Create Module';
      this.editModuleButtonText = 'Update Module';
    }
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
        this.viewOrder = result.view_order;
        this.viewDetails = result.view_details;

        for(let view of this.viewOrder) {
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
    this.activeView = this.viewOrder[this.openedPanelStep];
    this.addContentDialog = false;
    this.openedWeekStep = null;

    // Get content if view does not have any content
    // if (!this.hasContent(this.viewOrder[step])) {
    //   this.getContentOfView();
    // }
    this.getContentOfView();
    this.deleteWeekError = null;
    this.resetContentStatusText();
  }

  setOpenedWeekStep(step: number) {
    if (this.openedWeekStep === step) {
      this.openedWeekStep = null;
    } else {
      this.openedWeekStep = step;
    }
    this.addContentDialog = false;
    this.deleteWeekError = null;
  }

  toggleAddModule() {
    this.showAddModuleForm = !this.showAddModuleForm;
    this.openedPanelStep = null;
    this.addModuleError = null;
  }

  addModule(name: string) {
    this.addModuleIndicator = true;
    this.addModuleError = null;
    this.addModuleFormEvent.next('disable');
    this.instituteApiService.createSubjectModule(
      this.currentSubjectSlug,
      name
    ).subscribe(
      (result: CreateSubjectModuleResponse) => {
        this.addModuleIndicator = false;
        this.addModuleFormEvent.next('reset');
        const view = result.view;
        delete result['view'];
        this.viewDetails[view] = result;
        this.viewData[view] = {
          1: []
        };
        this.viewOrder.push(view);
        this.uiService.showSnackBar(
          'Module "' + result.name + '" added successfully!',
          2000
        );
        this.showAddModuleForm = false;
      },
      errors => {
        this.addModuleIndicator = false;
        this.addModuleFormEvent.next('enable');
        if (errors.error) {
          if (errors.error.error) {
            this.addModuleError = errors.error.error;
          } else {
            this.addModuleError = 'Unable to add module. Unknown error occured.';
          }
        } else {
          this.addModuleError = 'Unable to add module. Unknown error occured';
        }
      }
    )
  }

  toggleEditModule() {
    if (this.showEditModuleForm) {
      this.editDeleteModuleError = null;
      this.selectedModuleName = null;
    } else {
      this.selectedModuleName = this.viewDetails[this.viewOrder[this.openedPanelStep]].name;
    }
    this.showEditModuleForm = !this.showEditModuleForm;
  }

  editModule(moduleName: string) {
    this.editModuleIndicator = true;
    this.editModuleFormEvent.next('disable');
    this.editDeleteModuleError = null;
    const view = this.viewOrder[this.openedPanelStep];
    this.instituteApiService.editSubjectModuleName(
      this.currentSubjectSlug,
      view,
      moduleName
    ).subscribe(
      (result: {name: string}) => {
        this.editModuleIndicator = false;
        this.editModuleFormEvent.next('reset');
        const currentName = this.viewDetails[view].name;
        this.viewDetails[view].name = result.name;
        this.showEditModuleForm = false;
        this.uiService.showSnackBar(
          'Successfully renamed "' + currentName + '" to "' + result.name + '".',
          3000
        );
      },
      errors => {
        this.editModuleIndicator = false;
        this.editModuleFormEvent.next('enable');
        if (errors.error){
          if (errors.error.error) {
            this.editDeleteModuleError = errors.error.error;
          } else {
            this.editDeleteModuleError = 'Unknown error occured while updating module name.';
          }
        } else {
          this.editDeleteModuleError = 'Unknown error occured while updating module name.';
        }
      }
    )
  }

  resetContentStatusText() {
    this.contentError = null;
    this.contentSuccessText = null;
    this.editDeleteModuleError = null;
  }

  addWeek() {
    this.showAddWeekSpinner = true;
    this.resetContentStatusText();
    const view = this.viewOrder[this.openedPanelStep];
    this.instituteApiService.addSubjectModuleWeek(this.currentSubjectSlug, view).subscribe(
      (result: {week: number} )=> {
        this.showAddWeekSpinner = false;
        this.viewData[view][result.week] = [];
        this.viewDetails[view][result.week] = 0;
        this.viewDetails[view].weeks.push(result.week);
        this.uiService.showSnackBar(
          'Week added successfully.',
          3000
        );
      },
      errors => {
        this.showAddWeekSpinner = false;
        if (errors.error){
          if (errors.error.error) {
            this.contentError = errors.error.error;
          } else {
            this.contentError = 'Unknown error occured while adding week.';
          }
        } else {
          this.contentError = 'Unknown error occured while adding week.';
        }
      }
    )
  }

  confirmDeleteWeek(week: number, i: number) {
    const view = this.viewOrder[this.openedPanelStep];
    this.deleteWeekSubscription = this.uiService.dialogData$.subscribe(
      result => {
        if (result === true) {
          this.deleteWeek(view, week, i);
        }
        this.deleteWeekSubscription.unsubscribe();
      }
    );
    this.uiService.openDialog(
      'Are you sure you want to delete "Week ' + (i + 1).toString() + '" ?',
      'Cancel',
      'Delete'
    );
  }

  getIndexOfWeek(arr: Array<number>, key: number) {
    for(let i in arr) {
      if (arr[i] === key) {
        return i;
      }
    }
    return -1;
  }

  deleteWeek(view: string, week: number, visibleWeekNumber: number) {
    this.showDeleteWeekSpinner = true;
    this.deleteWeekError = null;
    this.instituteApiService.deleteWeekOfSubjectModule(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      view,
      week.toString()
    ).subscribe(
      () => {
        this.showDeleteWeekSpinner = false;
        this.viewDetails[view].count -= this.viewData[view][week].length;
        const index = this.getIndexOfWeek(
          this.viewDetails[view]['weeks'],
          week
        );
        if (index > -1) {
          this.viewDetails[view]['weeks'].splice(
            index, 1);
        }
        delete this.viewData[view][week];
        delete this.viewDetails[view][week];
        this.uiService.showSnackBar(
          'Successfully deleted "Week ' + visibleWeekNumber.toString() + '".',
          2000
        );
      },
      (errors: any) => {
        this.showDeleteWeekSpinner = false;
        if (errors.error) {
          if (errors.error.error) {
            this.deleteWeekError = errors.error.error;
          } else {
            this.deleteWeekError = 'Unable to delete week. Unknown error occured.';
          }
        } else {
          this.deleteWeekError = 'Unable to delete week. Unknown error occured.';
        }
      }
    )
  }

  confirmDeleteModule() {
    const view = this.viewOrder[this.openedPanelStep];
    this.deleteWeekSubscription = this.uiService.dialogData$.subscribe(
      result => {
        if (result === true) {
          this.deleteModule(view);
        }
        this.deleteWeekSubscription.unsubscribe();
      }
    );
    this.uiService.openDialog(
      'Are you sure you want to delete "' + this.viewDetails[view].name + '" ?',
      'Cancel',
      'Delete'
    );
  }

  deleteModule(view: string) {
    this.showDeleteModuleSpinner = true;
    this.editDeleteModuleError = null;
    const moduleName = this.viewDetails[view].name;
    this.instituteApiService.deleteSubjectModule(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      view
    ).subscribe(
      () => {
        this.showDeleteModuleSpinner = false;
        delete this.viewDetails[view];
        delete this.viewData[view];
        this.viewOrder.splice(this.viewOrder.indexOf(view), 1);
        this.uiService.showSnackBar(
          'Module "' + moduleName + '" deleted successfully!',
          2000
        );
      },
      errors => {
        this.showDeleteModuleSpinner = false;
        if (errors.error) {
          if (errors.error.error) {
            this.editDeleteModuleError = errors.error.error;
          } else {
            this.editDeleteModuleError = 'Unable to delete module. Unknown error occured.';
          }
        } else {
          this.editDeleteModuleError = 'Unable to delete module. Unknown error occured.';
        }
      }
    )
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
        (result: StudyMaterialDetails[]) => {
          this.showContentLoadingIndicator = false;
          this.viewData[view] = result;
          console.log(this.viewData);
        },
        errors => {
          this.showContentLoadingIndicator = false;
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
    const view = this.viewOrder[this.openedPanelStep];
    this.deleteDialogDataSubscription = this.uiService.dialogData$.subscribe(
      result => {
        if (result) {
          this.deleteStudyMaterial(content, view);
        }
        this.deleteDialogDataSubscription.unsubscribe();
      }
    );
    this.uiService.openDialog(
      'Are you sure you want to delete \"' + content.title + "\"?",
      'No',
      'Yes'
    );
  }

  deleteStudyMaterial(content: StudyMaterialDetails, view: string) {
    this.contentError = null;
    this.instituteApiService.deleteClassCourseContent(content.id.toString()).subscribe(
      () => {
        this.hideCloseContentLoadingErrorButton = false;
        if (content.week) {
          this.viewData[view][content.week].splice(
            this.findIdInArray(this.viewData[view][content.week], content.id), 1);
          this.viewDetails[content.view][content.week] -= 1;
        } else {
          this.viewData[view].splice(this.viewData[view].indexOf(actionContent), 1);
        }
        this.viewDetails[content.view]['count'] -= 1;
        this.uiService.showSnackBar(
          'Content deleted successfully!',
          2000
        );
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

  reorderClicked() {}

  showActionsClicked(content: StudyMaterialDetails) {  // For mobile view
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

  normalContentAdded(result: StudyMaterialDetails) {
    if (!result['week']) {
      this.viewData[result.view].push(result);
    } else {
      this.viewData[result.view][result.week].push(result);
      this.viewDetails[result['view']][result['week']] += 1;
    }
    this.viewDetails[result['view']].count += 1;
  }

  mediaContentAdded(result: any) {
    if (!result.body['week']) {
      this.viewData[result.body['view']].push(result.body);
    } else {
      this.viewData[result.body['view']][result.body['week']].push(result.body);
      this.viewDetails[result.body['view']][result.body['week']] += 1;
    }
    this.viewDetails[result.body['view']].count += 1;
  }

  toggleAddContentDialog() {
      this.addContentDialog = !this.addContentDialog;
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

  findIdInArray(array: Array<any>, id: number) {
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
      this.uiService.showSnackBar(
        'Content Deleted Successfully!',
        2000
      );
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

  hasContent(view: string) {
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

  hideDeleteWeekError() {
    this.deleteWeekError = null;
  }

  hideEditDeleteModuleError() {
    this.editDeleteModuleError = null;
  }

  hideAddModuleError() {
    this.addModuleError = null;
  }

  ngOnDestroy() {
    sessionStorage.removeItem(actionContent);
    sessionStorage.removeItem(activeCreateCourseView);
  }

}
