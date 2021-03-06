import { currentClassSlug, currentSubjectSlug, SUBJECT_TYPE_REVERSE, hasSubjectPerm, hasClassPerm, SUBJECT_TYPE, userId, currentInstituteRole, INSTITUTE_ROLE_REVERSE } from './../../../constants';
import { InstituteSubjectDetails } from './../../models/subject.model';
import { Component, OnInit } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { Subscription } from 'rxjs';
import { Router } from '@angular/router';
import { UiService } from 'src/app/services/ui.service';


@Component({
  selector: 'app-class-subjects',
  templateUrl: './class-subjects.component.html',
  styleUrls: ['./class-subjects.component.css']
})
export class ClassSubjectsComponent implements OnInit {

  mq: MediaQueryList;
  showLoadingIndicator: boolean;
  showReloadError: boolean;
  showReloadText = 'Unable to fetch subject list...';
  loadingText = 'Fetching Subject List...';
  currentClassSlug: string;
  subjectStep: number;
  subjectList: InstituteSubjectDetails[];
  errorText: string;
  showCreateSubjectFormMb: boolean;
  createSubjectIndicator: boolean;
  createSubjectForm: FormGroup;
  subscribedDialogData: Subscription;
  hasClassPerm: boolean;

  constructor(
    private media: MediaMatcher,
    private instituteApiService: InstituteApiService,
    private formBuilder: FormBuilder,
    private router: Router,
    private uiService: UiService
    ) {
    this.mq = this.media.matchMedia('(max-width: 768px)');
    this.currentClassSlug = sessionStorage.getItem(currentClassSlug);
    if (sessionStorage.getItem(hasClassPerm) === 'true') {
      this.hasClassPerm = true;
    } else {
      this.hasClassPerm = false;
    }
  }

  ngOnInit(): void {
    this.getSubjectList();
    this.createSubjectForm = this.formBuilder.group({
      name: [null, [Validators.required, Validators.maxLength(40)]],
      type: [false]
    });
  }

  getSubjectList() {
    this.showLoadingIndicator = true;
    this.showReloadError = false;
    this.errorText = null;
    this.instituteApiService.getSubjectList(this.currentClassSlug).subscribe(
      (result: InstituteSubjectDetails[]) => {
        this.showLoadingIndicator = false;
        this.subjectList = result;
      },
      errors => {
        this.showLoadingIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.errorText = errors.error.error;
          } else {
            this.showReloadError = true;
          }
        } else {
          this.showReloadError = true;
        }
      }
    );
  }

  createSubject() {
    this.createSubjectForm.patchValue({
      name: this.createSubjectForm.value.name.trim()
    });
    this.createSubjectIndicator = true;
    this.errorText = null;
    if (this.createSubjectForm.value.name.length > 0) {
      this.createSubjectForm.disable();
      let type: string;
      if (!this.createSubjectForm.value.type) {
        type = SUBJECT_TYPE_REVERSE.MANDATORY;
      } else {
        type = SUBJECT_TYPE_REVERSE.OPTIONAL;
      }
      this.instituteApiService.createSubject(
        this.currentClassSlug,
        this.createSubjectForm.value.name,
        type
        ).subscribe(
        (result: InstituteSubjectDetails) => {
          this.createSubjectIndicator = false;
          this.showReloadError = false;
          this.createSubjectForm.enable();
          this.createSubjectForm.reset();
          this.showCreateSubjectFormMb = false;
          if (!this.subjectList) {
            this.subjectList = [];
          }
          this.subjectList.push(result);
          this.uiService.showSnackBar(
            'Subject created successfully!',
            2000
          );
        },
        errors => {
          this.createSubjectIndicator = false;
          this.createSubjectForm.enable();
          if (errors.error) {
            if (errors.error.error) {
              this.errorText = errors.error.error;
            } else {
              this.errorText = 'Subject creation failed.';
            }
          } else {
            this.errorText = 'Subject creation failed.';
          }
        }
      );
    }
  }

  openSubject(subjectSlug: string, hasSubjectPermission: boolean) {
    sessionStorage.setItem(currentSubjectSlug, subjectSlug);
    if (hasSubjectPermission) {
      sessionStorage.setItem(hasSubjectPerm, 'true');
    } else {
      sessionStorage.setItem(hasSubjectPerm, 'false');
    }
    this.router.navigate(['subject-workspace/' + subjectSlug.slice(0, -10) + '/overview']);
  }

  showCreateSubjectFormMobile() {
    this.clearAllStatusText();
    this.showCreateSubjectFormMb = true;
  }

  hideCreateSubjectFormMobile() {
    this.clearAllStatusText();
    this.showCreateSubjectFormMb = false;
  }

  clearAllStatusText() {
    this.errorText = null;
  }


  // For handling expansion panel
  setSubjectStep(step: number) {
    this.subjectStep = step;
  }

  isSubjectListEmpty() {
    if (this.subjectList) {
      return this.subjectList.length === 0;
    } else {
      return false;
    }
  }

  closeErrorText() {
    this.errorText = null;
  }

  deleteSubjectClicked(subjectObject: InstituteSubjectDetails) {
    this.subscribedDialogData = this.uiService.dialogData$.subscribe(
      result => {
        if (result) {
          this.deleteSubject(subjectObject);
        }
        this.unsubscribeDialogData();
      }
    );
    const subjectName = subjectObject.name.charAt(0).toUpperCase() + subjectObject.name.substr(1).toLowerCase();
    const header = 'Are you sure you want to delete ' + subjectName + ' ?';
    this.uiService.openDialog(header, 'Cancel', 'Delete');
  }

  deleteSubject(subjectObject: InstituteSubjectDetails) {
    this.instituteApiService.deleteClass(subjectObject.subject_slug).subscribe(
      () => {
        this.uiService.showSnackBar('Deleted class ' + subjectObject.name.toUpperCase() + ' successfully!', 2000);
        this.subjectList.splice(this.subjectList.indexOf(subjectObject), 1);
      }
    );
  }

  unsubscribeDialogData() {
    if (this.subscribedDialogData) {
      this.subscribedDialogData.unsubscribe();
    }
  }

  getSubjectType(key: string) {
    return SUBJECT_TYPE[key];
  }

  hasSubjectIncharge(inchargeList: any) {
    if (inchargeList.length > 0) {
      return true;
    } else {
      return false;
    }
  }

  userIsNotSelf(id: number) {
    if (id.toString() === sessionStorage.getItem(userId)) {
      return false;
    } else {
      return true;
    }
  }

  userIsAdmin() {
    if (sessionStorage.getItem(currentInstituteRole) === INSTITUTE_ROLE_REVERSE.Admin) {
      return true;
    } else {
      return false;
    }
  }
}
