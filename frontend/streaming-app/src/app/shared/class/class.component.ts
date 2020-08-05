import { Subscription } from 'rxjs';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ClassDetailsResponse } from './../../models/class.model';
import { currentInstituteSlug, currentClassSlug, currentInstituteRole, INSTITUTE_ROLE_REVERSE } from './../../../constants';
import { InstituteApiService } from './../../services/institute-api.service';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';
import { UiService } from 'src/app/services/ui.service';

@Component({
  selector: 'app-class',
  templateUrl: './class.component.html',
  styleUrls: ['./class.component.css']
})
export class ClassComponent implements OnInit {

  mq: MediaQueryList;
  showLoadingIndicator: boolean;
  showReloadError: boolean;
  showReloadText = 'Unable to fetch class list...';
  loadingText = 'Fetching Class List...';
  currentInstituteSlug: string;
  classStep: number;
  classList: ClassDetailsResponse[] = [];
  errorText: string;
  successText: string;
  showCreateClassFormMb: boolean;
  createClassIndicator: boolean;
  createClassForm: FormGroup;
  subscribedDialogData: Subscription;

  constructor(
    private media: MediaMatcher,
    private instituteApiService: InstituteApiService,
    private formBuilder: FormBuilder,
    private router: Router,
    private uiService: UiService
    ) {
    this.mq = this.media.matchMedia('(max-width: 768px)');
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
  }

  ngOnInit(): void {
    this.getClassList();
    this.createClassForm = this.formBuilder.group({
      name: [null, [Validators.required, Validators.maxLength(40)]]
    })
  }

  getClassList() {
    this.showLoadingIndicator = true;
    this.showReloadError = false;
    this.errorText = null;
    this.instituteApiService.getInstituteClassList(this.currentInstituteSlug).subscribe(
      (result: ClassDetailsResponse[]) => {
        this.showLoadingIndicator = false;
        for(const class_ of result) {
          this.classList.push(class_);
        }
      },
      errors => {
        console.log(errors)
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
    )
  }

  createClass() {
    this.createClassForm.patchValue({
      name: this.createClassForm.value.name.trim()
    })
    this.createClassIndicator = true;
    this.errorText = null;
    this.successText = null;
    if (this.createClassForm.value.name.length > 0) {
      this.createClassForm.disable();
      this.instituteApiService.createInstituteClass(this.currentInstituteSlug, this.createClassForm.value.name).subscribe(
        (result: ClassDetailsResponse) => {
          this.createClassIndicator = false;
          this.successText = 'Class created successfully!';
          this.createClassForm.enable();
          this.createClassForm.reset();
          this.showCreateClassFormMb = false;
          this.classList.push(result);
        },
        errors => {
          this.createClassIndicator = false;
          this.createClassForm.enable();
          if (errors.error) {
            if (errors.error.error) {
              this.errorText = errors.error.error;
            } else {
              this.errorText = 'Class with same name exists.';
            }
          } else {
            this.errorText = 'Class creation failed.';
          }
        }
      )
    }
  }

  openClass(classSlug: string) {
    sessionStorage.setItem(currentClassSlug, classSlug);
    this.router.navigate(['class-workspace/' + classSlug.slice(0, -10) + '/profile']);
  }

  showCreateClassFormMobile() {
    this.clearAllStatusText();
    this.showCreateClassFormMb = true;
  }

  hideCreateClassFormMobile() {
    this.clearAllStatusText();
    this.showCreateClassFormMb = false;
  }

  clearAllStatusText() {
    this.errorText = null;
    this.successText = null;
  }


  // For handling expansion panel
  setClassStep(step: number) {
    this.classStep = step;
  }

  isClassesListEmpty() {
    return this.classList.length === 0;
  }

  closeErrorText() {
    this.errorText = null;
  }

  closeSuccessText() {
    this.successText = null;
  }

  userIsAdmin() {
    if (sessionStorage.getItem(currentInstituteRole) === INSTITUTE_ROLE_REVERSE['Admin']) {
      return true;
    } else {
      return false;
    }
  }

  deleteClassClicked(classObject: ClassDetailsResponse) {
    this.subscribedDialogData = this.uiService.dialogData$.subscribe(
      result => {
        if (result) {
          this.deleteClass(classObject);
        }
        this.unsubscribeDialogData();
      }
    )
    const header = 'Are you sure you want to delete ' + classObject.name.charAt(0).toUpperCase() + classObject.name.substr(1).toLowerCase() + ' ?';
    this.uiService.openDialog(header, 'Cancel', 'Delete');
  }

  deleteClass(classObject: ClassDetailsResponse) {
    this.instituteApiService.deleteClass(classObject.class_slug).subscribe(
      () => {
        this.uiService.showSnackBar('Deleted class ' + classObject.name.toUpperCase() + ' successfully!', 2000);
        this.classList.splice(this.classList.indexOf(classObject), 1);
      }
    )
  }

  unsubscribeDialogData() {
    if (this.subscribedDialogData) {
      this.subscribedDialogData.unsubscribe();
    }
  }
}
