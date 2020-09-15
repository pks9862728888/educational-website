import { hasSubjectPerm } from './../../../constants';
import { DownloadService } from './../../services/download.service';
import { Component, OnInit, Input, EventEmitter, Output } from '@angular/core';
import { StudyMaterialDetails } from '../../models/subject.model';
import { actionContent, currentSubjectSlug } from '../../../constants';
import { MediaMatcher } from '@angular/cdk/layout';
import { Subscription, Subject } from 'rxjs';
import { UiService } from 'src/app/services/ui.service';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { getFileSize } from 'src/app/shared/utilityFunctions';

@Component({
  selector: 'app-view-pdf',
  templateUrl: './view-pdf.component.html',
  styleUrls: ['./view-pdf.component.css']
})
export class ViewPdfComponent implements OnInit {

  hasSubjectPerm: boolean;
  content: StudyMaterialDetails;
  @Output() closeViewEvent = new EventEmitter();
  mq: MediaQueryList;
  errorText: string;
  successText: string;
  showEditForm = false;
  public formControlEvent = new Subject<string>();
  deleteConfirmationSubscription: Subscription;
  contentEdited: boolean;
  filename: string;

  constructor(
    private media: MediaMatcher,
    private uiService: UiService,
    private instituteApiService: InstituteApiService
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.content = JSON.parse(sessionStorage.getItem(actionContent));
    if (sessionStorage.getItem(hasSubjectPerm) === 'true') {
      this.hasSubjectPerm = true;
    } else {
      this.hasSubjectPerm = false;
    }
  }

  ngOnInit(): void {
    const ext = this.content.data.file.split('.');
    this.filename = this.content.title.toLowerCase().replace(' ', '_') + '.' + ext[ext.length - 1];
  }

  back() {
    if (this.contentEdited) {
      this.closeViewEvent.emit(this.content);
    } else {
      this.closeViewEvent.emit();
    }
  }

  toggleEditForm() {
    this.showEditForm = !this.showEditForm;
  }

  edit(eventData) {
    delete eventData['id'];
    this.formControlEvent.next('DISABLE');
    this.closeErrorText();
    this.closeSuccessText();
    this.instituteApiService.editSubjectCourseContent(
      eventData,
      sessionStorage.getItem(currentSubjectSlug),
      this.content.id.toString()
      ).subscribe(
        (result: StudyMaterialDetails) => {
          this.formControlEvent.next('RESET');
          this.showEditForm = false;
          this.successText = 'Content modified successfully!';
          this.content = result;
          this.contentEdited = true;
          sessionStorage.setItem(actionContent, JSON.stringify(this.content));
        },
        errors => {
          this.formControlEvent.next('ENABLE');
          if (errors.error) {
            if (errors.error.error) {
              this.errorText = errors.error.error;
            } else {
              this.errorText = 'Unable to edit at the moment.';
            }
          } else {
            this.errorText = 'Unable to edit at the moment.';
          }
        }
      )
  }

  confirmDelete() {
    this.deleteConfirmationSubscription = this.uiService.dialogData$.subscribe(
      result => {
        if (result) {
          this.delete();
          this.deleteConfirmationSubscription.unsubscribe();
        }
      }
    )
    this.uiService.openDialog(
      'Are you sure you want to delete \'' + this.content.title + "' ?",
      "Cancel",
      "Delete"
    );
  }

  delete() {
    this.instituteApiService.deleteSubjectIntroductoryContent(
      sessionStorage.getItem(currentSubjectSlug),
      this.content.id.toString()
      ).subscribe(
      () => {
        this.closeViewEvent.emit('DELETED');
      },
      errors => {
        if (errors.error) {
          if (errors.error.error) {
            this.errorText = errors.error.error;
          } else {
            this.errorText = 'Unable to delete at the moment.';
          }
        } else {
          this.errorText = 'Unable to delete at the moment.';
        }
      }
    )
  }

  closeErrorText() {
    this.errorText = null;
  }

  closeSuccessText() {
    this.successText = null;
  }

}
