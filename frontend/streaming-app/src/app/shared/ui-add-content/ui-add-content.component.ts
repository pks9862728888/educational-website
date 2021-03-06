import { currentSubjectSlug } from './../../../constants';
import { InstituteApiService } from './../../services/institute-api.service';
import { Subject } from 'rxjs';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { StudyMaterialDetails } from '../../models/subject.model';
import { HttpEventType } from '@angular/common/http';

@Component({
  selector: 'app-ui-add-content',
  templateUrl: './ui-add-content.component.html',
  styleUrls: ['./ui-add-content.component.css']
})
export class UiAddContentComponent implements OnInit {

  mq: MediaQueryList;
  currentSubjectSlug: string;
  contentSuccessText: string;
  uploadError: string;
  selectedSidenav = 'ADD_EXTERNAL_LINK';
  allowTargetDateSetting = false;

  @Input() view: string;

  uploadingEvent = new Subject<String>();
  uploadProgressEvent = new Subject<{loaded: number, total: number}>();
  @Output() contentAdded = new EventEmitter<any>();

  constructor(
    private media: MediaMatcher,
    private instituteApiService: InstituteApiService
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.currentSubjectSlug = sessionStorage.getItem(currentSubjectSlug);
  }

  uploadExternalLink(data: any) {
    data['view_key'] = this.view;
    this.uploadingEvent.next('DISABLE');
    this.uploadError = null;
    this.contentSuccessText = null;
    this.instituteApiService.addSubjectExternalLinkIntroductoryCourseContent(
      this.currentSubjectSlug,
      data
      ).subscribe(
        result => {
          this.uploadingEvent.next('RESET');
          this.contentSuccessText = 'Uploaded Successfully.';
          this.contentAdded.emit(result);
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

  uploadMediaFile(data: any) {
    data['view_key'] = this.view;

    this.uploadError = null;
    this.contentSuccessText = null;
    this.uploadingEvent.next('DISABLE');
    this.uploadProgressEvent.next({
      'total': data.size,
      'loaded': 0,
    });
    this.instituteApiService.uploadIntroductoryCourseContentMaterial(
      this.currentSubjectSlug,
      data
      ).subscribe(
      result => {
        if (result.type === HttpEventType.UploadProgress) {
          this.uploadProgressEvent.next({
            'total': result.total,
            'loaded': result.loaded,
          });
        } else if (result.type === HttpEventType.Response) {
          this.uploadingEvent.next('RESET');
          this.contentSuccessText = 'Upload successful.';
          this.contentAdded.emit(result);
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

  uploadFormError(data: string) {
    this.uploadError = data;
  }

  closeUploadError(event: any) {
    this.uploadError = null;
  }

  closeUploadSuccess(event: any) {
    this.contentSuccessText = null;
  }

  setActiveSidenav(text: string) {
    this.selectedSidenav = text;
  }

}
