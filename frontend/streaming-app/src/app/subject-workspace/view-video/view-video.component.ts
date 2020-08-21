import { actionContent, currentSubjectSlug } from './../../../constants';
import { Component, OnInit, EventEmitter, Output, OnDestroy, } from '@angular/core';
import { StudyMaterialDetails } from '../../models/subject.model';
import { MediaMatcher } from '@angular/cdk/layout';
import { Subscription, Subject } from 'rxjs';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { UiService } from 'src/app/services/ui.service';


declare const videojs: any;


@Component({
  selector: 'app-view-video',
  templateUrl: './view-video.component.html',
  styleUrls: ['./view-video.component.css']
})
export class ViewVideoComponent implements OnInit, OnDestroy {

  content: StudyMaterialDetails;
  @Output() closeViewEvent = new EventEmitter();
  mq: MediaQueryList;
  errorText: string;
  successText: string;
  showEditForm = false;
  public formControlEvent = new Subject<string>();
  deleteConfirmationSubscription: Subscription;
  player: any;
  contentEdited: boolean;


  constructor(
    private media: MediaMatcher,
    private uiService: UiService,
    private instituteApiService: InstituteApiService
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.content = JSON.parse(sessionStorage.getItem(actionContent));
  }

  ngOnInit(): void {
    this.player = videojs(document.getElementById('video-player'));
    this.player.src({
      src: this.content.data.stream_file,
      type: 'application/x-mpegURL'
    });
    this.player.hlsQualitySelector({
      displayCurrentQuality: true,
    });
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
    this.instituteApiService.deleteClassCourseContent(this.content.id.toString()).subscribe(
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

  ngOnDestroy() {
    this.player.dispose();
  }

}
