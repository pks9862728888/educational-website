import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, EventEmitter, Output, Input, OnDestroy } from '@angular/core';
import { Validators, FormGroup, FormBuilder } from '@angular/forms';
import { formatDate } from '../../format-datepicker';
import { Subscription, Observable } from 'rxjs';
import { SUBJECT_INTRODUCTION_CONTENT_TYPE_REVERSE } from '../../../constants';
import { getFileSize } from '../utilityFunctions';

@Component({
  selector: 'app-ui-upload-image',
  templateUrl: './ui-upload-image.component.html',
  styleUrls: ['./ui-upload-image.component.css']
})
export class UiUploadImageComponent implements OnInit, OnDestroy {

  mq: MediaQueryList;
  uploadForm: FormGroup;
  showIndicator: boolean;
  progress = 0;
  @Input() showTargetDate: boolean;
  @Output() formData = new EventEmitter<any>();
  @Output() fileError = new EventEmitter<string>();
  @Input() formEvent: Observable<string>;
  private formEventSubscription: Subscription;
  @Input() uploadProgressEvent: Observable<{loaded: number, total: number}>;
  private progressEventSubscription: Subscription;
  totalFileSize: number;
  loadedFileSize: number;

  constructor(
    private media: MediaMatcher,
    private formBuilder: FormBuilder
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.uploadForm = this.formBuilder.group({
      name: [null, [Validators.required, Validators.maxLength(30)]],
      file: [null, [Validators.required]],
      target_date: [null],
      description: [null],
      can_download: [true]
    });
    this.formEventSubscription = this.formEvent.subscribe(
      (data: string) => {
        if (data === 'ENABLE') {
          this.showIndicator = false;
          this.uploadForm.enable();
        } else if (data === 'DISABLE') {
          this.showIndicator = true;
          this.uploadForm.disable();
        } else if (data === 'RESET') {
          this.showIndicator = false;
          this.uploadForm.reset();
          this.uploadForm.enable();
          this.uploadForm.patchValue({
            can_download: true
          });
        }
      }
    );
    this.progressEventSubscription = this.uploadProgressEvent.subscribe(
      (result: {loaded: number, total: number}) => {
        this.progress = Math.round(100 * result.loaded / result.total);
        this.loadedFileSize = result.loaded;
        this.totalFileSize = result.total;
      }
    );
  }

  upload() {
    const file: File = (document.getElementById('image-file') as HTMLInputElement).files[0];

    if (!file.type.includes('image/jpeg') && !file.type.includes('image/jpg') && !file.type.includes('image/png')) {
      this.fileError.emit('Only .jpeg, .jpg, and .png formats are supported.');
      this.uploadForm.patchValue({
        file: null
      });
    } else {
      const data = {
        name: this.uploadForm.value.name,
        file,
        can_download: this.uploadForm.value.can_download,
        content_type: SUBJECT_INTRODUCTION_CONTENT_TYPE_REVERSE.IMAGE
      };
      if (this.uploadForm.value.target_date) {
        data['target_date'] = formatDate(this.uploadForm.value.target_date);
      }
      this.formData.emit(data);
    }
  }

  getFileSize_(size: number) {
    return getFileSize(size);
  }

  ngOnDestroy() {
    if (this.formEventSubscription) {
      this.formEventSubscription.unsubscribe();
    }
    if (this.progressEventSubscription) {
      this.progressEventSubscription.unsubscribe();
    }
  }
}
