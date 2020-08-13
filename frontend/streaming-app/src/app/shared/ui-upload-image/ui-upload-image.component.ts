import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, EventEmitter, Output, Input, OnDestroy } from '@angular/core';
import { Validators, FormGroup, FormBuilder } from '@angular/forms';
import { formatDate } from '../../format-datepicker';
import { Subscription, Observable } from 'rxjs';

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
    console.log(file);
    console.log(formatDate(this.uploadImageForm.value.target_date));

    if (!file.type.includes('image/jpeg') && !file.type.includes('image/jpg') && !file.type.includes('image/png') && !file.type.includes('image/webp')) {
      this.fileError.emit('Only .jpeg, .jpg, .webp, and .png formats are supported.');
      this.uploadImageForm.patchValue({
        file: null
      });
    } else {
      alert(file.size / 1000000);
      this.formData.emit(file.size / 1000000000 + ' GB');
    }
  }

  ngOnDestroy() {
    if (this.formEventSubscription) {
      this.formEventSubscription.unsubscribe();
    }
  }
}
