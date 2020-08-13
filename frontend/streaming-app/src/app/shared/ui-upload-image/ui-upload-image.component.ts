import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, EventEmitter, Output, Input, OnDestroy } from '@angular/core';
import { Validators, FormGroup, FormBuilder } from '@angular/forms';
import { formatDate } from '../../format-datepicker';
import { Subscription, Observable } from 'rxjs';
import { STUDY_MATERIAL_CONTENT_TYPE_REVERSE } from '../../../constants';

@Component({
  selector: 'app-ui-upload-image',
  templateUrl: './ui-upload-image.component.html',
  styleUrls: ['./ui-upload-image.component.css']
})
export class UiUploadImageComponent implements OnInit, OnDestroy {

  mq: MediaQueryList;
  uploadImageForm: FormGroup;
  showIndicator: boolean;
  @Input() showTargetDate: boolean;
  @Output() formData = new EventEmitter<any>();
  @Output() fileError = new EventEmitter<string>();
  @Input() formEvent: Observable<String>;
  private formEventSubscription: Subscription;
  private fileSize: number;

  constructor(
    private media: MediaMatcher,
    private formBuilder: FormBuilder
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.uploadImageForm = this.formBuilder.group({
      title: [null, [Validators.required, Validators.maxLength(30)]],
      file: [null, [Validators.required]],
      target_date: [null]
    });
    this.formEventSubscription = this.formEvent.subscribe(
      (data: string) => {
        if (data === 'ENABLE') {
          this.showIndicator = false;
          this.uploadImageForm.enable();
        } else if (data === 'DISABLE') {
          this.showIndicator = true;
          this.uploadImageForm.disable();
        } else if (data === 'RESET') {
          this.showIndicator = false;
          this.uploadImageForm.reset();
          this.uploadImageForm.enable();
        }
      }
    );
  }

  upload() {
    const file: File = (<HTMLInputElement>document.getElementById('image-file')).files[0];

    if (!file.type.includes('image/jpeg') && !file.type.includes('image/jpg') && !file.type.includes('image/png') && !file.type.includes('image/webp')) {
      this.fileError.emit('Only .jpeg, .jpg, .webp, and .png formats are supported.');
      this.uploadImageForm.patchValue({
        file: null
      });
    } else {
      this.fileSize = file.size;
      let data = this.uploadImageForm.value;
      if (this.uploadImageForm.value.target_date) {
        data['target_date'] = formatDate(this.uploadImageForm.value.target_date);
      }
      data['size'] = file.size / 1000000000;
      data['content_type'] = STUDY_MATERIAL_CONTENT_TYPE_REVERSE['IMAGE'];
      this.formData.emit(data);
    }
  }

  getFileSize() {
    if (this.fileSize >= 1000000000) {
      return this.fileSize / 1000000000 + ' GB';
    } else if (this.fileSize >= 1000000) {
      return this.fileSize / 1000000 + ' MB';
    } else if (this.fileSize >= 1000) {
      return this.fileSize / 1000 + ' KB';
    } else {
      return this.fileSize + ' bytes';
    }
  }

  ngOnDestroy() {
    if (this.formEventSubscription) {
      this.formEventSubscription.unsubscribe();
    }
  }
}
