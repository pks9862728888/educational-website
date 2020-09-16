import { formatDate } from 'src/app/format-datepicker';
import { currentSubjectSlug, STUDY_MATERIAL_VIEW_TYPES, currentInstituteSlug, LECTURE_TEXT_TYPES, LECTURE_LINK_TYPES, LECTURE_STUDY_MATERIAL_TYPES } from './../../../constants';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { UiService } from 'src/app/services/ui.service';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { Subject, Subscription } from 'rxjs';
import { CreateSubjectCourseMinDetailsResponse, CreateSubjectModuleResponse, InstituteSubjectLectureContentData, InstituteSubjectLectureMaterial } from 'src/app/models/subject.model';
import { isContentTypeExternalLink, isContentTypeImage, isContentTypeLink, isContentTypePdf, isContentTypeYouTubeLink } from 'src/app/shared/utilityFunctions';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Url } from 'url';
import { HttpEventType } from '@angular/common/http';

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
  selectedLecture: any;

  currentSubjectSlug: string;
  currentInstituteSlug: string;

  openedPanelStep: number;
  editContentError: boolean;
  editContentIndex: number;

  showAddModuleForm = false;
  addModuleError: string;
  addModuleIndicator: boolean;
  addModuleFormEvent = new Subject<string>();

  showEditModuleForm: boolean;
  editModuleIndicator: boolean;
  editDeleteModuleError: string;
  editModuleFormEvent = new Subject<string>();
  editContentFormEvent = new Subject<string>();

  showDeleteModuleSpinner: boolean;
  deleteModuleSubscription: Subscription;

  addContentDialog: boolean;
  addContentSuccessText: string;
  uploadError: string;

  showContentLoadingIndicator: boolean;
  contentReload: string;

  loadingViewContentIndicator: boolean;
  loadingContentError: string;
  reloadContent: boolean;

  deleteDialogDataSubscription: Subscription;

  showAddLectureForm: boolean;
  addLectureForm: FormGroup;
  showAddLectureIndicator: boolean;
  deleteLectureSubscription: Subscription;

  editLectureForm: FormGroup;
  showEditLectureIndicator: boolean;

  isContentTypeImage = isContentTypeImage;
  isContentTypePdf = isContentTypePdf;
  isContentTypeLink = isContentTypeLink;
  isContentTypeYouTubeLink = isContentTypeYouTubeLink;
  isContentTypeExternalLink = isContentTypeExternalLink;
  minDate = new Date();

  hasSubjectPerm: boolean;
  viewOrder: Array<string> = [];
  testViews: Array<string> = [];
  viewDetails = {};
  introductionViewData = {};
  lectureViewData = {};
  testDetails = {};

  // For lecture
  loadingLectureContentIndicator: boolean;
  reloadLectureContent: boolean;
  loadLectureError: string;

  addEditObjectiveForm: FormGroup;
  showaddEditObjectiveForm = false;
  showAddObjectiveIndicator: boolean;
  showEditObjectiveForm: boolean;

  addEditUseCaseForm: FormGroup;
  showaddEditUseCaseForm = false;
  showAddUseCaseIndicator: boolean;
  showEditUseCaseForm: boolean;

  addEditAdditionalReadingForm: FormGroup;
  showaddEditAdditionalReadingForm = false;
  showAddAdditionalReadingIndicator: boolean;
  showEditAdditionalReadingForm: boolean;

  addEditGetInspiredForm: FormGroup;
  showaddEditGetInspiredForm = false;
  showAddGetInspiredIndicator: boolean;
  showEditGetInspiredForm: boolean;

  showaddEditLectureContentForm = false;
  showAddLectureContentIndicator: boolean;
  showEditLectureContentForm: boolean;
  selectedSidenav: string;
  uploadingEvent = new Subject<String>();
  uploadProgressEvent = new Subject<{loaded: number, total: number}>();
  editLectureContentForm: FormGroup;

  lectureContentData: InstituteSubjectLectureContentData;

  constructor(
    private media: MediaMatcher,
    private uiService: UiService,
    private instituteApiService: InstituteApiService,
    private formBuilder: FormBuilder
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.currentSubjectSlug = sessionStorage.getItem(currentSubjectSlug);
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
  }

  ngOnInit(): void {
    this.getMinCourseDetails();
    this.addLectureForm = this.formBuilder.group({
      name: ['', [Validators.required, Validators.maxLength(30)]],
      target_date: ['']
    });
    this.editLectureForm = this.formBuilder.group({
      name: ['', [Validators.required, Validators.maxLength(30)]],
      target_date: ['']
    });
    this.addEditObjectiveForm = this.formBuilder.group({
      text: ['', [Validators.required, Validators.maxLength(500)]]
    });
    this.addEditUseCaseForm = this.formBuilder.group({
      text: ['', [Validators.required, Validators.maxLength(500)]]
    });
    this.addEditAdditionalReadingForm = this.formBuilder.group({
      name: ['', [Validators.required, Validators.maxLength(100)]],
      link: ['', [Validators.required, Validators.maxLength(2083)]]
    });
    this.addEditGetInspiredForm = this.formBuilder.group({
      name: ['', [Validators.required, Validators.maxLength(100)]],
      link: ['', [Validators.required, Validators.maxLength(2083)]]
    });
    this.editLectureContentForm = this.formBuilder.group({
      name: ['', [Validators.required, Validators.maxLength(100)]],
      link: ['', [Validators.maxLength(1024)]],
      can_download: [false]
    });
  }

  getMinCourseDetails() {
    this.showLoadingIndicator = true;
    this.showReload = false;
    this.errorText = null;
    this.instituteApiService.getMinCourseDetails(this.currentSubjectSlug).subscribe(
      (result: CreateSubjectCourseMinDetailsResponse) => {
        this.showLoadingIndicator = false;
        this.hasSubjectPerm = result.has_subject_perm;
        this.viewOrder = result.view_order;
        this.viewDetails = result.view_details;
        this.testViews = result.test_views;
        this.testDetails = result.test_details;

        for (let view of this.viewOrder) {
          if (!this.testViews.includes(view)) {
            if (view === 'MI' || view === 'CO') {
              this.introductionViewData[view] = [];
            } else {
              this.lectureViewData[view] = [];
            }
          }
        }
        console.log(result);
        console.log(this.viewOrder);
        console.log(this.viewDetails);
        console.log(this.testViews);
        console.log(this.testDetails);
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
    );
  }

  toggleEditModule() {
    if (this.showEditModuleForm) {
      this.editDeleteModuleError = null;
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
    );
  }

  editClicked(content) {
    const view = this.viewOrder[this.openedPanelStep];
    if (this.editContentIndex !== null && this.editContentIndex !== undefined) {
      if (view === 'MI' || view === 'CO') {
        this.introductionViewData[view][this.editContentIndex]['edit'] = false;
      } else {
        this.lectureViewData[view][this.editContentIndex]['edit'] = false;
      }
    }
    if (view === 'MI' || view === 'CO') {
      this.editContentIndex = +this.findIdInArray(this.introductionViewData[view], content.id);
      this.introductionViewData[view][this.editContentIndex]['edit'] = true;
    } else {
      this.editContentIndex = +this.findIdInArray(this.lectureViewData[view], content.id);
      this.lectureViewData[view][this.editContentIndex]['edit'] = true;
    }
  }

  closeEditForm(content) {
    const view = this.viewOrder[this.openedPanelStep];
    if (view === 'MI' || view === 'CO') {
      this.introductionViewData[view][this.editContentIndex]['edit'] = false;
    } else {
      this.lectureViewData[view][this.editContentIndex]['edit'] = false;
    }
    this.editContentIndex = null;
  }

  updateContent(eventData: any) {
    const view = this.viewOrder[this.openedPanelStep];
    this.editContentFormEvent.next('DISABLE');
    this.editContentError = null;

    this.instituteApiService.editSubjectCourseContent(
      eventData,
      this.currentSubjectSlug,
      eventData['id'].toString()
      ).subscribe(
        result => {
          console.log(result);
          this.editContentFormEvent.next('RESET');
          this.uiService.showSnackBar(
            'Content updated successfully!',
            2000
          );
          this.closeEditForm(eventData);
          if (view === 'MI' || view === 'CO') {
            this.introductionViewData[view].splice(
              this.findIdInArray(this.introductionViewData[view], result['id']),
              1,
              result
            );
          } else {
            this.lectureViewData[view].splice(
              this.findIdInArray(this.lectureViewData[view], result['id']),
              1,
              result
            );
          }
        },
        errors => {
          this.editContentFormEvent.next('ENABLE');
          if (errors.error) {
            if (errors.error.error) {
              this.uiService.showSnackBar(
                errors.error.error,
                3000
              );
            } else {
              this.uiService.showSnackBar(
                'Unable to edit at the moment.',
                3000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Unable to edit at the moment.',
              3000
            );
          }
        }
      )
  }

  deleteClicked(content) {
    const view = this.viewOrder[this.openedPanelStep];
    this.deleteDialogDataSubscription = this.uiService.dialogData$.subscribe(
      result => {
        if (result) {
          this.deleteIntroductoryContentMaterial(content, view);
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

  findIdInArray(array: Array<any>, id: number) {
    for(let idx in array) {
      if (array[idx]['id'] === id) {
        return idx;
      }
    }
    return -1;
  }

  deleteIntroductoryContentMaterial(content, view: string) {
    this.instituteApiService.deleteSubjectIntroductoryContent(
      this.currentSubjectSlug,
      content.id.toString()
      ).subscribe(
      () => {
        const index = this.findIdInArray(this.introductionViewData[view], content.id);
        this.introductionViewData[view].splice(index, 1);
        this.viewDetails[view]['count'] -= 1;
        this.uiService.showSnackBar(
          'Content deleted successfully!',
          2000
        );
      },
      errors => {
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(
              errors.error.error,
              3000
            );
          } else {
            this.uiService.showSnackBar(
              'Unable to delete at the moment. Please try again later.',
              3000
            );
          }
        } else {
          this.uiService.showSnackBar(
            'Unable to delete at the moment. Please try again later.',
            3000
          );
        }
      }
    );
  }

  showActionsClicked() {

  }

  setOpenedPanelStep(step: number) {
    this.showEditModuleForm = false;
    this.showDeleteModuleSpinner = false;
    this.addContentSuccessText = null;
    this.uploadError = null;
    this.addContentDialog = false;
    this.editContentIndex = null;
    this.showEditLectureIndicator = false;
    this.addLectureForm.reset();
    this.editLectureForm.reset();
    if (this.openedPanelStep === step) {
      this.openedPanelStep = null;
    } else {
      this.openedPanelStep = step;
      this.getViewContents();
    }
  }

  getViewContents() {
    this.loadingViewContentIndicator = false;
    this.loadingContentError = null;
    this.reloadContent = false;
    const view = this.viewOrder[this.openedPanelStep];
    this.instituteApiService.getCourseContentOfSpecificView(
      this.currentSubjectSlug,
      view)
      .subscribe(
        result => {
          this.loadingViewContentIndicator = false;
          if (view === 'MI' || view === 'CO') {
            this.introductionViewData[view] = result;
            this.updateStats(view);
          } else {
            this.lectureViewData[view] = result;
          }
          console.log(result);
          console.log(this.introductionViewData);
          console.log(this.lectureViewData);
        },
        errors => {
          this.loadingViewContentIndicator = false;
          if (errors.errors) {
            if (errors.errors.error) {
              this.loadingContentError = errors.error.error;
            } else {
              this.reloadContent = true;
            }
          } else {
            this.reloadContent = true;
          }
        }
      );
  }

  updateStats(view: string) {
    let count = 0;
    if (view === 'MI' || view === 'CO') {
      count = this.introductionViewData[view].length;
    } else {
      count = this.lectureViewData[view].length;
    }
    this.viewDetails[view].count = count;
  }

  toggleAddContentDialog() {
    this.addContentDialog = !this.addContentDialog;
    this.addContentSuccessText = null;
    this.uploadError = null;
  }

  introductoryContentAdded(result: any) {
    if (result.body) {
      this.introductionViewData[result['body']['view']].push(result['body']);
      this.viewDetails[result['body']['view']].count += 1;
    } else {
      this.introductionViewData[result['view']].push(result);
      this.viewDetails[result['view']].count += 1;
    }
    console.log(result);
    console.log(this.introductionViewData);
  }

  addModule(name: string) {
    this.addModuleIndicator = true;
    this.addModuleError = null;
    this.addModuleFormEvent.next('disable');
    this.instituteApiService.createSubjectModule(
      this.currentSubjectSlug,
      name,
      STUDY_MATERIAL_VIEW_TYPES.MODULE_VIEW
    ).subscribe(
      (result: CreateSubjectModuleResponse) => {
        this.addModuleIndicator = false;
        this.addModuleFormEvent.next('reset');
        const view = result.view;
        delete result['view'];
        this.viewDetails[view] = result;
        this.viewOrder.push(view);
        this.lectureViewData[view] = [];
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
    );
  }

  toggleAddModule() {
    this.showAddModuleForm = !this.showAddModuleForm;
    this.openedPanelStep = null;
    this.addModuleError = null;
  }

  confirmDeleteModule() {
    const view = this.viewOrder[this.openedPanelStep];
    this.deleteModuleSubscription = this.uiService.dialogData$.subscribe(
      result => {
        if (result === true) {
          this.deleteModule(view);
        }
        this.deleteModuleSubscription.unsubscribe();
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
        delete this.lectureViewData[view];
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

  addLectureClicked() {
    this.showAddLectureForm = true;
  }

  addLecture() {
    this.addLectureForm.patchValue({
      name: this.addLectureForm.value.name.trim()
    });
    if (!this.addLectureForm.invalid) {
      let data = this.addLectureForm.value;
      const view = this.viewOrder[this.openedPanelStep];
      data['view_key'] = view;
      if (data.target_date) {
        data['target_date'] = formatDate(data.target_date);
      }
      this.showAddLectureIndicator = true;
      this.instituteApiService.addSubjectLecture(
        this.currentSubjectSlug,
        data
      ).subscribe(
        result => {
          this.showAddLectureIndicator = false;
          this.lectureViewData[view].push(result);
          this.viewDetails[view].count += 1;
          this.closeAddLecture();
          this.uiService.showSnackBar(
            'Lecture added successfully!',
            2000
          );
        },
        errors => {
          this.showAddLectureIndicator = false;
          if (errors.error) {
            if (errors.error.error) {
              this.uiService.showSnackBar(
                errors.error.error,
                3000
              );
            } else {
              this.uiService.showSnackBar(
                'Unable to add lecture at the moment.',
                3000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Unable to add lecture at the moment.',
              3000
            );
          }
        }
      )
    }
  }

  confirmDeleteLecture(lecture) {
    const view = this.viewOrder[this.openedPanelStep];
    this.deleteLectureSubscription = this.uiService.dialogData$.subscribe(
      result => {
        if (result === true) {
          this.deleteLecture(lecture, view);
        }
        this.deleteLectureSubscription.unsubscribe();
      }
    );
    this.uiService.openDialog(
      'Are you sure you want to delete lecture "' + lecture.name + '" ?',
      'Cancel',
      'Delete'
    );
  }

  deleteLecture(lecture, view: string) {
    const index = this.findIdInArray(this.lectureViewData[view], lecture.id);
    this.lectureViewData[view][index]['delete'] = true;
    this.instituteApiService.deleteSubjectLecture(
      this.currentSubjectSlug,
      lecture.id.toString()
    ).subscribe(
      () => {
        this.lectureViewData[view].splice(index, 1);
        this.uiService.showSnackBar(
          'Lecture "' + lecture.name + '" deleted successfully!',
          2000
        );
        this.viewDetails[view].count -= 1;
      },
      errors => {
        this.lectureViewData[view][index]['delete'] = false;
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(
              errors.error.error,
              3000
            );
          } else {
            this.uiService.showSnackBar(
              'Unable to delete module. Unknown error occured.',
              3000
            );
          }
        } else {
          this.uiService.showSnackBar(
            'Unable to delete module. Unknown error occured.',
            3000
          );
        }
      }
    )
  }

  editLectureClicked(content) {
    const view = this.viewOrder[this.openedPanelStep];
    this.editLectureForm.patchValue({
      name: content.name,
      target_date: content.target_date
    });

    for (let index in this.lectureViewData[view]) {
      if (this.lectureViewData[view][index].id !== content.id) {
        this.lectureViewData[view][index]['edit'] = false;
      } else {
        this.lectureViewData[view][index]['edit'] = true;
      }
    }
  }

  editLecture(content) {
    this.editLectureForm.patchValue({
      name: this.editLectureForm.value.name.trim()
    });
    if (!this.editLectureForm.invalid) {
      const view = this.viewOrder[this.openedPanelStep];
      let data = this.editLectureForm.value;
      if (data.target_date) {
        data.target_date = formatDate(data.target_date);
      }
      this.showEditLectureIndicator = true;
      this.instituteApiService.editSubjectLecture(
        this.currentSubjectSlug,
        content.id.toString(),
        data
      ).subscribe(
        result => {
          this.showEditLectureIndicator = false;
          const index = this.findIdInArray(this.lectureViewData[view], content.id);
          this.lectureViewData[view].splice(index, 1, result);
          this.uiService.showSnackBar(
            'Lecture updated Successfully!',
            2000
          );
        },
        errors => {
          this.showEditLectureIndicator = false;
          if (errors.error) {
            if (errors.error.error) {
              this.uiService.showSnackBar(
                errors.error.error,
                3000
              );
            } else {
              this.uiService.showSnackBar(
                'Unable to edit lecture. Unknown error occured.',
                3000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Unable to edit lecture. Unknown error occured.',
              3000
            );
          }
        }
      )
    }
  }

  closeEditLecture(content) {
    const view = this.viewOrder[this.openedPanelStep];
    const index = this.findIdInArray(this.lectureViewData[view], content.id);
    this.lectureViewData[view][index]['edit'] = false;
    this.editLectureForm.reset();
  }

  hideAddModuleError() {
    this.addModuleError = null;
  }

  closeErrorText() {
    this.errorText = null;
  }

  closeEditContentError() {
    this.editContentError = null;
  }

  closeAddLecture() {
    this.addLectureForm.reset();
    this.showAddLectureForm = false;
  }

  // For lecture view
  openLecture(content, lecture_no) {
    content['lecture_no'] = lecture_no;
    this.selectedLecture = content;
    this.loadLectureContent();
  }

  closeLecture() {
    this.selectedLecture = null;
    this.addEditObjectiveForm.reset();
    this.showaddEditObjectiveForm = false;
  }

  loadLectureContent() {
    this.loadingLectureContentIndicator = true;
    this.reloadLectureContent = false;
    this.loadingContentError = null;
    this.instituteApiService.loadSubjectLectureContents(
      this.currentSubjectSlug,
      this.selectedLecture.id.toString()
    ).subscribe(
      (result: InstituteSubjectLectureContentData) => {
        this.loadingLectureContentIndicator = false;
        this.lectureContentData = result;
        console.log(this.lectureContentData);
      },
      errors => {
        this.loadingLectureContentIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.loadingContentError = errors.error.error;
          } else {
            this.reloadLectureContent = true;
          }
        } else {
          this.reloadLectureContent = true;
        }
      }
    );
  }

  toggleAddCourseObjectiveForm() {
    this.addEditObjectiveForm.reset();
    this.addEditObjectiveForm.enable();
    this.showAddObjectiveIndicator = false;
    this.showaddEditObjectiveForm = !this.showaddEditObjectiveForm;
    this.closeEditObjectiveForm();
  }

  addLectureObjective() {
    this.addEditObjectiveForm.patchValue({
      text: this.addEditObjectiveForm.value.text.trim()
    });
    if (!this.addEditObjectiveForm.invalid) {
      let data = this.addEditObjectiveForm.value;
      data['type'] = LECTURE_TEXT_TYPES['OBJECTIVES'];
      this.addEditObjectiveForm.disable();
      this.showAddObjectiveIndicator = true;
      this.instituteApiService.addLectureObjectiveOrUseCase(
        this.currentSubjectSlug,
        this.selectedLecture.id.toString(),
        data
      ).subscribe(
        (result: {id: number; text: string;}) => {
          this.lectureContentData.objectives.push(result);
          this.uiService.showSnackBar(
            'Objective added!',
            2000
          );
          this.toggleAddCourseObjectiveForm();
        },
        errors => {
          this.showAddObjectiveIndicator = false;
          if (errors.error) {
            if (errors.error.error) {
              this.uiService.showSnackBar(
                errors.error.error,
                3000
              );
            } else {
              this.uiService.showSnackBar(
                'Error occurred! Unable to add objectives now.',
                3000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Error occurred! Unable to add objectives now.',
              3000
            );
          }
        }
      );
    }
  }

  deleteObjective(content) {
    const index = +this.findIdInArray(this.lectureContentData.objectives, content.id);
    this.lectureContentData.objectives[index]['delete'] = true;
    this.instituteApiService.deleteObjectiveOrUseCase(
      this.currentSubjectSlug,
      content.id.toString()
    ).subscribe(
      () => {
        for (let index in this.lectureContentData.objectives) {
          if (this.lectureContentData.objectives[index]['edit']) {
            if (this.lectureContentData.objectives[index].id === content.id) {
              this.showEditObjectiveForm = false;
            }
          }
        }
        this.lectureContentData.objectives.splice(index, 1);
        this.uiService.showSnackBar(
          'Objective deleted!',
          2000
        );
      },
      errors => {
        this.lectureContentData.objectives[index]['delete'] = false;
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(
              errors.error.error,
              3000
            );
          } else {
            this.uiService.showSnackBar(
              'Error occurred! Unable to delete objectives now.',
              3000
            );
          }
        } else {
          this.uiService.showSnackBar(
            'Error occurred! Unable to delete objectives now.',
            3000
          );
        }
      }
    )
  }

  showEditObjectiveFormClicked(objective) {
    this.addEditObjectiveForm.reset();
    this.addEditObjectiveForm.enable();
    this.showAddObjectiveIndicator = false;
    this.showaddEditObjectiveForm = false;
    this.addEditObjectiveForm.patchValue({
      text: objective.text
    });
    this.showEditObjectiveForm = true;
    for (let idx in this.lectureContentData.objectives) {
      if (this.lectureContentData.objectives[idx].id === objective.id) {
        this.lectureContentData.objectives[idx]['edit'] = true;
      } else {
        this.lectureContentData.objectives[idx]['edit'] = false;
      }
    }
  }

  closeEditObjectiveForm() {
    this.showEditObjectiveForm = false;
    for (let idx in this.lectureContentData.objectives) {
      if (this.lectureContentData.objectives[idx]['edit']) {
        this.lectureContentData.objectives[idx]['edit'] = false;
      }
    }
  }

  editLectureObjective() {
    this.addEditObjectiveForm.patchValue({
      text: this.addEditObjectiveForm.value.text.trim()
    });
    if (!this.addEditObjectiveForm.invalid) {
      this.showAddObjectiveIndicator = true;
      this.addEditObjectiveForm.disable();
      let objective_id = -1;
      let index = -1;
      for (let idx in this.lectureContentData.objectives) {
        if (this.lectureContentData.objectives[idx]['edit']) {
          index = +idx;
          objective_id = this.lectureContentData.objectives[idx].id;
        }
      }
      let data = this.addEditObjectiveForm.value;
      this.instituteApiService.editObjectiveOrUseCase(
        this.currentSubjectSlug,
        objective_id.toString(),
        data
      ).subscribe(
        (result: {id: number; text: string;}) => {
          this.lectureContentData.objectives.splice(index, 1, result);
          this.uiService.showSnackBar(
            'Objective updated',
            2000
          );
          this.showEditObjectiveForm = false;
        },
        errors => {
          this.addEditObjectiveForm.enable();
          this.showAddObjectiveIndicator = false;
          if (errors.error) {
            if (errors.error.error) {
              this.uiService.showSnackBar(
                errors.error.error,
                3000
              );
            } else {
              this.uiService.showSnackBar(
                'Error occurred! Unable to edit objectives now.',
                3000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Error occurred! Unable to edit objectives now.',
              3000
            );
          }
        }
      );
    }
  }

  toggleAddCourseUseCaseForm() {
    this.addEditUseCaseForm.reset();
    this.addEditUseCaseForm.enable();
    this.showAddUseCaseIndicator = false;
    this.showaddEditUseCaseForm = !this.showaddEditUseCaseForm;
    this.closeEditUseCaseForm();
  }

  addLectureUseCase() {
    this.addEditUseCaseForm.patchValue({
      text: this.addEditUseCaseForm.value.text.trim()
    });
    if (!this.addEditUseCaseForm.invalid) {
      let data = this.addEditUseCaseForm.value;
      data['type'] = LECTURE_TEXT_TYPES['USE_CASE'];
      this.addEditUseCaseForm.disable();
      this.showAddUseCaseIndicator = true;
      this.instituteApiService.addLectureObjectiveOrUseCase(
        this.currentSubjectSlug,
        this.selectedLecture.id.toString(),
        data
      ).subscribe(
        (result: {id: number; text: string;}) => {
          this.lectureContentData.use_case_text.push(result);
          this.uiService.showSnackBar(
            'Use Case added!',
            2000
          );
          this.toggleAddCourseUseCaseForm();
        },
        errors => {
          this.showAddUseCaseIndicator = false;
          if (errors.error) {
            if (errors.error.error) {
              this.uiService.showSnackBar(
                errors.error.error,
                3000
              );
            } else {
              this.uiService.showSnackBar(
                'Error occurred! Unable to add use case now.',
                3000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Error occurred! Unable to add use case now.',
              3000
            );
          }
        }
      );
    }
  }

  deleteUseCase(content) {
    const index = +this.findIdInArray(this.lectureContentData.use_case_text, content.id);
    this.lectureContentData.use_case_text[index]['delete'] = true;
    this.instituteApiService.deleteObjectiveOrUseCase(
      this.currentSubjectSlug,
      content.id.toString()
    ).subscribe(
      () => {
        for (let index in this.lectureContentData.use_case_text) {
          if (this.lectureContentData.use_case_text[index]['edit']) {
            if (this.lectureContentData.use_case_text[index].id === content.id) {
              this.showEditUseCaseForm = false;
            }
          }
        }
        this.lectureContentData.use_case_text.splice(index, 1);
        this.uiService.showSnackBar(
          'Use case deleted!',
          2000
        );
      },
      errors => {
        this.lectureContentData.use_case_text[index]['delete'] = false;
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(
              errors.error.error,
              3000
            );
          } else {
            this.uiService.showSnackBar(
              'Error occurred! Unable to delete use case now.',
              3000
            );
          }
        } else {
          this.uiService.showSnackBar(
            'Error occurred! Unable to delete use case now.',
            3000
          );
        }
      }
    )
  }

  showEditUseCaseFormClicked(use_case) {
    this.addEditUseCaseForm.reset();
    this.addEditUseCaseForm.enable();
    this.showAddUseCaseIndicator = false;
    this.showaddEditUseCaseForm = false;
    this.addEditUseCaseForm.patchValue({
      text: use_case.text
    });
    this.showEditUseCaseForm = true;
    for (let idx in this.lectureContentData.use_case_text) {
      if (this.lectureContentData.use_case_text[idx].id === use_case.id) {
        this.lectureContentData.use_case_text[idx]['edit'] = true;
      } else {
        this.lectureContentData.use_case_text[idx]['edit'] = false;
      }
    }
  }

  closeEditUseCaseForm() {
    this.showEditUseCaseForm = false;
    for (let idx in this.lectureContentData.use_case_text) {
      if (this.lectureContentData.use_case_text[idx]['edit']) {
        this.lectureContentData.use_case_text[idx]['edit'] = false;
      }
    }
  }

  editLectureUseCase() {
    this.addEditUseCaseForm.patchValue({
      text: this.addEditUseCaseForm.value.text.trim()
    });
    if (!this.addEditUseCaseForm.invalid) {
      this.showAddUseCaseIndicator = true;
      this.addEditUseCaseForm.disable();
      let use_case_id = -1;
      let index = -1;
      for (let idx in this.lectureContentData.use_case_text) {
        if (this.lectureContentData.use_case_text[idx]['edit']) {
          index = +idx;
          use_case_id = this.lectureContentData.use_case_text[idx].id;
        }
      }
      let data = this.addEditUseCaseForm.value;
      this.instituteApiService.editObjectiveOrUseCase(
        this.currentSubjectSlug,
        use_case_id.toString(),
        data
      ).subscribe(
        (result: {id: number; text: string;}) => {
          this.lectureContentData.use_case_text.splice(index, 1, result);
          this.uiService.showSnackBar(
            'Use case updated.',
            2000
          );
          this.showEditUseCaseForm = false;
        },
        errors => {
          this.addEditUseCaseForm.enable();
          this.showAddUseCaseIndicator = false;
          if (errors.error) {
            if (errors.error.error) {
              this.uiService.showSnackBar(
                errors.error.error,
                3000
              );
            } else {
              this.uiService.showSnackBar(
                'Error occurred! Unable to edit use case now.',
                3000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Error occurred! Unable to edit use case now.',
              3000
            );
          }
        }
      );
    }
  }

  toggleAddCourseAdditionalReadingForm() {
    this.addEditAdditionalReadingForm.reset();
    this.addEditAdditionalReadingForm.enable();
    this.showAddAdditionalReadingIndicator = false;
    this.showaddEditAdditionalReadingForm = !this.showaddEditAdditionalReadingForm;
    this.closeEditAdditionalReadingForm();
  }

  addLectureAdditionalReadingLink() {
    this.addEditAdditionalReadingForm.patchValue({
      name: this.addEditAdditionalReadingForm.value.name.trim(),
      link: this.addEditAdditionalReadingForm.value.link.trim()
    });
    if (!this.addEditAdditionalReadingForm.invalid) {
      let data = this.addEditAdditionalReadingForm.value;
      data['type'] = LECTURE_LINK_TYPES['ADDITIONAL_READING_LINK'];
      this.addEditAdditionalReadingForm.disable();
      this.showAddAdditionalReadingIndicator = true;
      this.instituteApiService.addLectureAdditionalReadingOrUseCaseLink(
        this.currentSubjectSlug,
        this.selectedLecture.id.toString(),
        data
      ).subscribe(
        (result: {id: number; name: string; link: string;}) => {
          this.lectureContentData.additional_reading_link.push(result);
          this.uiService.showSnackBar(
            'Additional reading link added!',
            2000
          );
          this.toggleAddCourseAdditionalReadingForm();
        },
        errors => {
          this.showAddAdditionalReadingIndicator = false;
          if (errors.error) {
            if (errors.error.error) {
              this.uiService.showSnackBar(
                errors.error.error,
                3000
              );
            } else {
              this.uiService.showSnackBar(
                'Error occurred! Unable to add additional reading link now.',
                3000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Error occurred! Unable to add additional reading link now.',
              3000
            );
          }
        }
      );
    }
  }

  deleteAdditionalReadingLink(content) {
    const index = +this.findIdInArray(this.lectureContentData.additional_reading_link, content.id);
    this.lectureContentData.additional_reading_link[index]['delete'] = true;
    this.instituteApiService.deleteAdditionalReadingOrUseCaseLink(
      this.currentSubjectSlug,
      content.id.toString()
    ).subscribe(
      () => {
        for (let index in this.lectureContentData.additional_reading_link) {
          if (this.lectureContentData.additional_reading_link[index]['edit']) {
            if (this.lectureContentData.additional_reading_link[index].id === content.id) {
              this.showEditAdditionalReadingForm = false;
            }
          }
        }
        this.lectureContentData.additional_reading_link.splice(index, 1);
        this.uiService.showSnackBar(
          'Additional reading link deleted!',
          2000
        );
      },
      errors => {
        this.lectureContentData.additional_reading_link[index]['delete'] = false;
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(
              errors.error.error,
              3000
            );
          } else {
            this.uiService.showSnackBar(
              'Error occurred! Unable to delete additional reading link now.',
              3000
            );
          }
        } else {
          this.uiService.showSnackBar(
            'Error occurred! Unable to delete additional reading link now.',
            3000
          );
        }
      }
    )
  }

  showEditAdditionalReadingFormClicked(additional_reading) {
    this.addEditAdditionalReadingForm.reset();
    this.addEditAdditionalReadingForm.enable();
    this.showAddAdditionalReadingIndicator = false;
    this.showaddEditAdditionalReadingForm = false;
    this.addEditAdditionalReadingForm.patchValue({
      name: additional_reading.name,
      link: additional_reading.link
    });
    this.showEditAdditionalReadingForm = true;
    for (let idx in this.lectureContentData.additional_reading_link) {
      if (this.lectureContentData.additional_reading_link[idx].id === additional_reading.id) {
        this.lectureContentData.additional_reading_link[idx]['edit'] = true;
      } else {
        this.lectureContentData.additional_reading_link[idx]['edit'] = false;
      }
    }
  }

  closeEditAdditionalReadingForm() {
    this.showEditAdditionalReadingForm = false;
    for (let idx in this.lectureContentData.additional_reading_link) {
      if (this.lectureContentData.additional_reading_link[idx]['edit']) {
        this.lectureContentData.additional_reading_link[idx]['edit'] = false;
      }
    }
  }

  editLectureAdditionalReading() {
    this.addEditAdditionalReadingForm.patchValue({
      name: this.addEditAdditionalReadingForm.value.name.trim(),
      link: this.addEditAdditionalReadingForm.value.link.trim()
    });
    if (!this.addEditAdditionalReadingForm.invalid) {
      this.showAddAdditionalReadingIndicator = true;
      this.addEditAdditionalReadingForm.disable();
      let additional_reading_id = -1;
      let index = -1;
      for (let idx in this.lectureContentData.additional_reading_link) {
        if (this.lectureContentData.additional_reading_link[idx]['edit']) {
          index = +idx;
          additional_reading_id = this.lectureContentData.additional_reading_link[idx].id;
        }
      }
      let data = this.addEditAdditionalReadingForm.value;
      this.instituteApiService.editAdditionalReadingOrUseCaseLink(
        this.currentSubjectSlug,
        additional_reading_id.toString(),
        data
      ).subscribe(
        (result: {id: number; name: string; link: string;}) => {
          this.lectureContentData.additional_reading_link.splice(index, 1, result);
          this.uiService.showSnackBar(
            'Additional reading link updated',
            2000
          );
          this.showEditAdditionalReadingForm = false;
        },
        errors => {
          this.addEditAdditionalReadingForm.enable();
          this.showAddAdditionalReadingIndicator = false;
          if (errors.error) {
            if (errors.error.error) {
              this.uiService.showSnackBar(
                errors.error.error,
                3000
              );
            } else {
              this.uiService.showSnackBar(
                'Error occurred! Unable to edit additional reading link now.',
                3000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Error occurred! Unable to edit additional reading link now.',
              3000
            );
          }
        }
      );
    }
  }

  toggleAddCourseGetInspiredForm() {
    this.addEditGetInspiredForm.reset();
    this.addEditGetInspiredForm.enable();
    this.showAddGetInspiredIndicator = false;
    this.showaddEditGetInspiredForm = !this.showaddEditGetInspiredForm;
    this.closeEditGetInspiredForm();
  }

  addLectureGetInspiredLink() {
    this.addEditGetInspiredForm.patchValue({
      name: this.addEditGetInspiredForm.value.name.trim(),
      link: this.addEditGetInspiredForm.value.link.trim()
    });
    if (!this.addEditGetInspiredForm.invalid) {
      let data = this.addEditGetInspiredForm.value;
      data['type'] = LECTURE_LINK_TYPES['USE_CASES_LINK'];
      this.addEditGetInspiredForm.disable();
      this.showAddGetInspiredIndicator = true;
      this.instituteApiService.addLectureAdditionalReadingOrUseCaseLink(
        this.currentSubjectSlug,
        this.selectedLecture.id.toString(),
        data
      ).subscribe(
        (result: {id: number; name: string; link: string;}) => {
          this.lectureContentData.use_case_link.push(result);
          this.uiService.showSnackBar(
            'Get Inspired link added!',
            2000
          );
          this.toggleAddCourseGetInspiredForm();
        },
        errors => {
          this.showAddGetInspiredIndicator = false;
          if (errors.error) {
            if (errors.error.error) {
              this.uiService.showSnackBar(
                errors.error.error,
                3000
              );
            } else {
              this.uiService.showSnackBar(
                'Error occurred! Unable to add get inspired link now.',
                3000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Error occurred! Unable to add get inspired link now.',
              3000
            );
          }
        }
      );
    }
  }

  deleteGetInspiredLink(content) {
    const index = +this.findIdInArray(this.lectureContentData.use_case_link, content.id);
    this.lectureContentData.use_case_link[index]['delete'] = true;
    this.instituteApiService.deleteAdditionalReadingOrUseCaseLink(
      this.currentSubjectSlug,
      content.id.toString()
    ).subscribe(
      () => {
        for (let index in this.lectureContentData.use_case_link) {
          if (this.lectureContentData.use_case_link[index]['edit']) {
            if (this.lectureContentData.use_case_link[index].id === content.id) {
              this.showEditGetInspiredForm = false;
            }
          }
        }
        this.lectureContentData.use_case_link.splice(index, 1);
        this.uiService.showSnackBar(
          'Get inspired link deleted!',
          2000
        );
      },
      errors => {
        this.lectureContentData.use_case_link[index]['delete'] = false;
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(
              errors.error.error,
              3000
            );
          } else {
            this.uiService.showSnackBar(
              'Error occurred! Unable to delete get inspired link now.',
              3000
            );
          }
        } else {
          this.uiService.showSnackBar(
            'Error occurred! Unable to delete get inspired link now.',
            3000
          );
        }
      }
    )
  }

  showEditGetInspiredFormClicked(use_case_link) {
    this.addEditGetInspiredForm.reset();
    this.addEditGetInspiredForm.enable();
    this.showAddGetInspiredIndicator = false;
    this.showaddEditGetInspiredForm = false;
    this.addEditGetInspiredForm.patchValue({
      name: use_case_link.name,
      link: use_case_link.link
    });
    this.showEditGetInspiredForm = true;
    for (let idx in this.lectureContentData.use_case_link) {
      if (this.lectureContentData.use_case_link[idx].id === use_case_link.id) {
        this.lectureContentData.use_case_link[idx]['edit'] = true;
      } else {
        this.lectureContentData.use_case_link[idx]['edit'] = false;
      }
    }
  }

  closeEditGetInspiredForm() {
    this.showEditGetInspiredForm = false;
    for (let idx in this.lectureContentData.use_case_link) {
      if (this.lectureContentData.use_case_link[idx]['edit']) {
        this.lectureContentData.use_case_link[idx]['edit'] = false;
      }
    }
  }

  editLectureGetInspired() {
    this.addEditAdditionalReadingForm.patchValue({
      name: this.addEditGetInspiredForm.value.name.trim(),
      link: this.addEditGetInspiredForm.value.link.trim()
    });
    if (!this.addEditGetInspiredForm.invalid) {
      this.showAddGetInspiredIndicator = true;
      this.addEditGetInspiredForm.disable();
      let get_inspired_id = -1;
      let index = -1;
      for (let idx in this.lectureContentData.use_case_link) {
        if (this.lectureContentData.use_case_link[idx]['edit']) {
          index = +idx;
          get_inspired_id = this.lectureContentData.use_case_link[idx].id;
        }
      }
      let data = this.addEditGetInspiredForm.value;
      this.instituteApiService.editAdditionalReadingOrUseCaseLink(
        this.currentSubjectSlug,
        get_inspired_id.toString(),
        data
      ).subscribe(
        (result: {id: number; name: string; link: string;}) => {
          this.lectureContentData.use_case_link.splice(index, 1, result);
          this.uiService.showSnackBar(
            'Get inspired link updated.',
            2000
          );
          this.showEditGetInspiredForm = false;
        },
        errors => {
          this.addEditGetInspiredForm.enable();
          this.showAddGetInspiredIndicator = false;
          if (errors.error) {
            if (errors.error.error) {
              this.uiService.showSnackBar(
                errors.error.error,
                3000
              );
            } else {
              this.uiService.showSnackBar(
                'Error occurred! Unable to edit get inspired link now.',
                3000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Error occurred! Unable to edit get inspired link now.',
              3000
            );
          }
        }
      );
    }
  }

  toggleAddCourseLectureContentForm() {
    this.showAddLectureContentIndicator = false;
    this.showaddEditLectureContentForm = !this.showaddEditLectureContentForm;
    this.closeEditLectureContentForm();
    this.selectedSidenav = 'YOUTUBE_LINK';
  }

  closeEditLectureContentForm() {
    this.showEditLectureContentForm = false;
    for (let idx in this.lectureContentData.materials) {
      if (this.lectureContentData.materials[idx]['edit']) {
        this.lectureContentData.materials[idx]['edit'] = false;
      }
    }
  }

  setActiveSidenav(option: string) {
    this.selectedSidenav = option;
  }

  uploadFormError(data: string) {
    this.uiService.showSnackBar(
      data,
      3000
    );
  }

  uploadExternalLinkLectureMaterial(data: any) {
    if (this.selectedSidenav === 'YOUTUBE_LINK') {
      data['content_type'] = LECTURE_STUDY_MATERIAL_TYPES['YOUTUBE_LINK'];
    } else if (this.selectedSidenav === 'EXTERNAL_LINK') {
      data['content_type'] = LECTURE_STUDY_MATERIAL_TYPES['EXTERNAL_LINK'];
    }
    this.uploadingEvent.next('DISABLE');
    this.instituteApiService.addExternalLinkCourseContent(
      this.currentSubjectSlug,
      this.selectedLecture.id.toString(),
      data
      ).subscribe(
        (result: InstituteSubjectLectureMaterial) => {
          this.uploadingEvent.next('RESET');
          this.uiService.showSnackBar(
            'Link Added Successfully',
            2000
          );
          this.lectureContentData.materials.push(result);
          this.toggleAddCourseLectureContentForm();
        },
        errors => {
          this.uploadingEvent.next('ENABLE');
          if(errors.error) {
            if (errors.error.error) {
              this.uiService.showSnackBar(
                errors.error.error,
                3000
              );
            } else {
              this.uiService.showSnackBar(
                'Unable to upload. Please try again.',
                3000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Unable to upload. Please try again.',
              3000
            );
          }
        }
      )
  }

  uploadMediaFileLectureMaterial(data: any) {
    if (this.selectedSidenav === 'PDF') {
      data['content_type'] = LECTURE_STUDY_MATERIAL_TYPES['PDF']
    } else if (this.selectedSidenav === 'IMAGE') {
      data['content_type'] = LECTURE_STUDY_MATERIAL_TYPES['IMAGE']
    }
    this.uploadingEvent.next('DISABLE');
    this.uploadProgressEvent.next({
      'total': data.size,
      'loaded': 0,
    });
    this.instituteApiService.uploadMediaCourseContentMaterial(
      this.currentSubjectSlug,
      this.selectedLecture.id.toString(),
      data
      ).subscribe(
      (result: any) => {
        if (result.type === HttpEventType.UploadProgress) {
          this.uploadProgressEvent.next({
            'total': result.total,
            'loaded': result.loaded,
          });
        } else if (result.type === HttpEventType.Response) {
          this.uploadingEvent.next('RESET');
          this.uiService.showSnackBar(
            'Upload successful.',
            2000
          );
          this.lectureContentData.materials.push(result.body);
          console.log(this.lectureContentData.materials);
          this.toggleAddCourseLectureContentForm();
        }
      },
      errors => {
        this.uploadingEvent.next('ENABLE');
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(
              errors.error.error,
              3000
            );
          } else {
            this.uiService.showSnackBar(
              'Error. Unable to upload at the moment.',
              3000
            );
          }
        } else {
          this.uiService.showSnackBar(
            'Error. Unable to upload at the moment.',
            3000
          );
        }
      }
    )
  }

  deleteLectureContent(content) {
    const index = +this.findIdInArray(this.lectureContentData.materials, content.id);
    this.lectureContentData.materials[index]['delete'] = true;
    this.instituteApiService.deleteLectureContent(
      this.currentSubjectSlug,
      content.id.toString()
    ).subscribe(
      () => {
        for (let index in this.lectureContentData.materials) {
          if (this.lectureContentData.materials[index]['edit']) {
            if (this.lectureContentData.materials[index].id === content.id) {
              this.showaddEditLectureContentForm = false;
            }
          }
        }
        this.lectureContentData.materials.splice(index, 1);
        this.uiService.showSnackBar(
          'Lecture content deleted!',
          2000
        );
      },
      errors => {
        this.lectureContentData.materials[index]['delete'] = false;
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(
              errors.error.error,
              3000
            );
          } else {
            this.uiService.showSnackBar(
              'Error occurred! Unable to delete lecture content now.',
              3000
            );
          }
        } else {
          this.uiService.showSnackBar(
            'Error occurred! Unable to delete lecture content now.',
            3000
          );
        }
      }
    )
  }

  showEditLectureContentFormClicked(content) {
    this.showAddLectureContentIndicator = false;
    this.showaddEditLectureContentForm = false;
    this.showAddGetInspiredIndicator = false;
    this.showaddEditLectureContentForm = false;
    if (content.content_type === LECTURE_STUDY_MATERIAL_TYPES['EXTERNAL_LINK'] ||
        content.content_type === LECTURE_STUDY_MATERIAL_TYPES['YOUTUBE_LINK']) {
          this.editLectureContentForm.patchValue({
            link: content.data.link,
            name: content.name
          });
    } else if (content.content_type === LECTURE_STUDY_MATERIAL_TYPES['PDF'] ||
               content.content_type === LECTURE_STUDY_MATERIAL_TYPES['IMAGE']) {
          this.editLectureContentForm.patchValue({
            name: content.name,
            can_download: content.data.can_download
          });
    }
    this.showEditLectureContentForm = true;
    for (let idx in this.lectureContentData.materials) {
      if (this.lectureContentData.materials[idx].id === content.id) {
        this.lectureContentData.materials[idx]['edit'] = true;
      } else {
        this.lectureContentData.materials[idx]['edit'] = false;
      }
    }
  }

  editLectureContent() {
    let data = this.editLectureContentForm.value;
    let index = -1;
    let contentId = -1;
    let content_type = '';
    for (let idx in this.lectureContentData.materials) {
      if (this.lectureContentData.materials[idx]['edit']) {
        index = +idx;
        contentId = this.lectureContentData.materials[idx].id;
        content_type = this.lectureContentData.materials[idx].content_type;
        if (this.lectureContentData.materials[idx].content_type === LECTURE_STUDY_MATERIAL_TYPES['EXTERNAL_LINK'] ||
            this.lectureContentData.materials[idx].content_type === LECTURE_STUDY_MATERIAL_TYPES['YOUTUBE_LINK']) {
            delete data['can_download'];
            this.editLectureContentForm.patchValue({
              name: this.editLectureContentForm.value.name.trim(),
              link: this.editLectureContentForm.value.link.trim()
            });
            if (!this.editLectureContentForm.value.link) {
              return;
            }
        } else if (this.lectureContentData.materials[idx].content_type === LECTURE_STUDY_MATERIAL_TYPES['PDF'] ||
                   this.lectureContentData.materials[idx].content_type === LECTURE_STUDY_MATERIAL_TYPES['IMAGE']) {
            this.editLectureContentForm.patchValue({
              name: this.editLectureContentForm.value.name.trim()
            });
            delete data['link'];
            if (!data['can_download']) {
              data['can_download'] = false;
            }
        }
      }
    }
    if (!this.editLectureContentForm.invalid) {
      data['content_type'] = content_type;
      console.log(data);
      this.showEditLectureIndicator = true;
      this.editLectureContentForm.disable();
      this.instituteApiService.editSubjectLectureContent(
        this.currentSubjectSlug,
        contentId.toString(),
        data
      ).subscribe(
        (result: any) => {
          this.showEditLectureIndicator = false;
          this.editLectureContentForm.reset();
          this.editLectureContentForm.enable();
          this.lectureContentData.materials.splice(index, 1, result);
          this.showEditLectureContentForm = false;
          this.uiService.showSnackBar(
            'Lecture content updated successfully.',
            3000
          );
        },
        errors => {
          this.showEditLectureIndicator = false;
          this.editLectureContentForm.enable();
          if (errors.error) {
            if (errors.error.error) {
              this.uiService.showSnackBar(
                errors.error.error,
                3000
              );
            } else {
              if (errors.error.error){
                this.uiService.showSnackBar(
                  'Unable to edit lecture content.',
                  3000
                );
              }
            }
          } else {
            if (errors.error.error){
              this.uiService.showSnackBar(
                'Unable to edit lecture content.',
                3000
              );
            }
          }
        }
      );
    }
  }

  isEditContentLink() {
    for (let content of this.lectureContentData.materials) {
      if (content['edit']) {
        if (content.content_type === LECTURE_STUDY_MATERIAL_TYPES['EXTERNAL_LINK'] ||
            content.content_type === LECTURE_STUDY_MATERIAL_TYPES['YOUTUBE_LINK']) {
              return true;
            } else {
              return false;
            }
      }
    }
    return false;
  }

  isEditContentFile() {
    for (let content of this.lectureContentData.materials) {
      if (content['edit']) {
        if (content.content_type === LECTURE_STUDY_MATERIAL_TYPES['IMAGE'] ||
            content.content_type === LECTURE_STUDY_MATERIAL_TYPES['PDF']) {
              return true;
            } else {
              return false;
            }
      }
    }
    return false;
  }

  openLinkInNewTab(link: Url) {
    window.open('//' + link, '_blank');
  }
}
