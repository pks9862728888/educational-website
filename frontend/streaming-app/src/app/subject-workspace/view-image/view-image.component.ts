import { InstituteApiService } from './../../services/institute-api.service';
import { UiService } from './../../services/ui.service';
import { DownloadService } from './../../services/download.service';
import { actionContent } from './../../../constants';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, EventEmitter, Output, ElementRef, ViewChild, OnDestroy } from '@angular/core';
import { StudyMaterialDetails } from '../../models/subject.model';
import { Subject, Subscription } from 'rxjs';
import { saveAs } from 'file-saver';

@Component({
  selector: 'app-view-image',
  templateUrl: './view-image.component.html',
  styleUrls: ['./view-image.component.css']
})
export class ViewImageComponent implements OnInit {

  content: StudyMaterialDetails;
  @Output() closeViewEvent = new EventEmitter();
  mq: MediaQueryList;
  errorText: string;
  successText: string;
  showEditForm = false;
  public formControlEvent = new Subject<string>();
  deleteConfirmationSubscription: Subscription;

  @ViewChild('downloadFile') private downloadLink: ElementRef;

  constructor(
    private media: MediaMatcher,
    private uiService: UiService,
    private instituteApiService: InstituteApiService
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.content = JSON.parse(sessionStorage.getItem(actionContent));
  }

  ngOnInit(): void {}

  back() {
    this.closeViewEvent.emit();
  }

  toggleEditForm() {
    this.showEditForm = !this.showEditForm;
  }

  edit(event) {
    alert('edit value');
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

}
