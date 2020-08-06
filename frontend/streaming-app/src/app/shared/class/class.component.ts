import { Subscription, Subject } from 'rxjs';
import { Router } from '@angular/router';
import { ClassDetailsResponse, ClassInchargeDetails } from './../../models/class.model';
import { currentInstituteSlug, currentClassSlug, currentInstituteRole, INSTITUTE_ROLE_REVERSE, hasClassPerm, userId } from './../../../constants';
import { InstituteApiService } from './../../services/institute-api.service';
import { Component, OnInit } from '@angular/core';
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
  subscribedDialogData: Subscription;
  inputPlaceholder = 'Class Name';
  createButtonText: string;
  createProgressSpinnerText = 'Creating class...';
  maxClassNameLength = 40;
  formEvent = new Subject<string>();

  constructor(
    private media: MediaMatcher,
    private instituteApiService: InstituteApiService,
    private router: Router,
    private uiService: UiService
    ) {
    this.mq = this.media.matchMedia('(max-width: 768px)');
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    if (this.mq.matches) {
      this.createButtonText = 'Create';
    } else {
      this.createButtonText = 'Create Class';
    }
  }

  ngOnInit(): void {
    this.getClassList();
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

  createClass(className: string) {
    this.createClassIndicator = true;
    this.errorText = null;
    this.successText = null;
    this.formEvent.next('disable');
    this.instituteApiService.createInstituteClass(this.currentInstituteSlug, className).subscribe(
      (result: ClassDetailsResponse) => {
        this.createClassIndicator = false;
        this.successText = 'Class created successfully!';
        this.showCreateClassFormMb = false;
        this.classList.push(result);
        this.formEvent.next('reset');
      },
      errors => {
        this.createClassIndicator = false;
        this.formEvent.next('enable');
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

  openClass(classSlug: string, hasClassPerm_: boolean) {
    sessionStorage.setItem(currentClassSlug, classSlug);
    if (hasClassPerm_) {
      sessionStorage.setItem(hasClassPerm, 'true');
    } else {
      sessionStorage.setItem(hasClassPerm, 'false');
    }
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

  classHasIncharge(inchargeList: ClassInchargeDetails[]) {
    if (inchargeList.length > 0) {
      return true;
    } else {
      return false;
    }
  }

  userIsSelf(id: number) {
    if (sessionStorage.getItem(userId) === id.toString()) {
      return true;
    } else {
      return false;
    }
  }
}
