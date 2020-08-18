import { DownloadService } from './../../services/download.service';
import { Component, OnInit, Input, EventEmitter, Output } from '@angular/core';
import { StudyMaterialDetails } from '../../models/subject.model';
import { actionContent, currentSubjectSlug } from '../../../constants';
import { MediaMatcher } from '@angular/cdk/layout';
import { Subscription, Subject } from 'rxjs';
import { UiService } from 'src/app/services/ui.service';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { PDFDocumentProxy, PDFProgressData } from 'ng2-pdf-viewer';
import { getFileSize } from 'src/app/shared/utilityFunctions';

@Component({
  selector: 'app-view-pdf',
  templateUrl: './view-pdf.component.html',
  styleUrls: ['./view-pdf.component.css']
})
export class ViewPdfComponent implements OnInit {

  content: StudyMaterialDetails;
  @Output() closeViewEvent = new EventEmitter();
  mq: MediaQueryList;
  errorText: string;
  successText: string;
  showEditForm = false;
  public formControlEvent = new Subject<string>();
  deleteConfirmationSubscription: Subscription;
  contentEdited: boolean;

  // For pdf viewer
  page = 1;
  zoom = 1;
  totalPages: number;
  downloadProgress = 0;
  loadedBytes = 0;
  totalBytes = 0;


  constructor(
    private media: MediaMatcher,
    private uiService: UiService,
    private downloadService: DownloadService,
    private instituteApiService: InstituteApiService
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.content = JSON.parse(sessionStorage.getItem(actionContent));
  }

  ngOnInit(): void {}

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
    this.formControlEvent.next('DISABLE');
    this.closeErrorText();
    this.closeSuccessText();
    this.instituteApiService.editSubjectCourseContent(
      eventData,
      sessionStorage.getItem(currentSubjectSlug),
      this.content.id
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

  delete() {
    this.deleteConfirmationSubscription = this.uiService.dialogData$.subscribe(
      result => {
        if (result === true) {
          this.instituteApiService.deleteClassCourseContent(this.content.id.toString()).subscribe(
            () => {
              this.closeViewEvent.emit('DELETED');
              this.unsubscribeDeleteConfirmation();
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
              this.unsubscribeDeleteConfirmation();
            }
          )
        }
      }
    )
    this.uiService.openDialog(
      'Are you sure you want to delete \'' + this.content.title + "' ?",
      "Cancel",
      "Delete"
    );
  }

  download() {
    const ext = this.content.data.file.split('.');
    saveAs(
      this.content.data.file, this.content.title.toLowerCase().replace(' ', '_') + '.' + ext[ext.length - 1]);
  }

  closeErrorText() {
    this.errorText = null;
  }

  closeSuccessText() {
    this.successText = null;
  }

  unsubscribeDeleteConfirmation() {
    if (this.deleteConfirmationSubscription) {
      this.deleteConfirmationSubscription.unsubscribe();
    }
  }

  incrementPage() {
    this.page = Math.min(this.totalPages, this.page + 1);
  }

  decrementPage() {
    this.page = Math.max(1, this.page - 1);
  }

  zoomIn() {
    this.zoom += 0.1;
  }

  zoomOut() {
    this.zoom = Math.max(0.4, this.zoom - 0.1);
  }

  zoomOriginalSize() {
    this.zoom = 1;
  }

  afterLoadComplete(pdf: PDFDocumentProxy) {
    this.totalPages = pdf.numPages;
  }

  onProgress(progressData: PDFProgressData) {
    this.downloadProgress = 100 * progressData.loaded / progressData.total;
    this.loadedBytes = progressData.loaded;
    this.totalBytes = progressData.total;
  }

  getLoadedFileSize() {
    return getFileSize(this.loadedBytes);
  }

  getTotalFileSize() {
    return getFileSize(this.totalBytes);
  }

}
