import { MediaMatcher } from '@angular/cdk/layout';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Component, OnInit, EventEmitter, Output, Input, OnDestroy } from '@angular/core';
import { formatDate } from '../../format-datepicker';
import { Subscription, Observable } from 'rxjs';


@Component({
  selector: 'app-ui-upload-video',
  templateUrl: './ui-upload-video.component.html',
  styleUrls: ['./ui-upload-video.component.css']
})
export class UiUploadVideoComponent implements OnInit, OnDestroy {

  mq: MediaQueryList;
  uploadVideoForm: FormGroup;
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
    this.uploadVideoForm = this.formBuilder.group({
      title: [null, [Validators.maxLength(30), Validators.required]],
      file: [null, [Validators.required]],
      target_date: [null]
    });
    this.formEventSubscription = this.formEvent.subscribe(
      (data: string) => {
        if (data === 'ENABLE') {
          this.showIndicator = false;
          this.uploadVideoForm.enable();
        } else if (data === 'DISABLE') {
          this.showIndicator = true;
          this.uploadVideoForm.disable();
        } else if (data === 'RESET') {
          this.showIndicator = false;
          this.uploadVideoForm.reset();
          this.uploadVideoForm.enable();
        }
      }
    );
  }

  upload() {
    const file: File = (<HTMLInputElement>document.getElementById('video-file')).files[0];
    console.log(file);
    console.log(formatDate(this.uploadVideoForm.value.target_date));

    // if (!file.type.includes('video/mp4') && !file.name.includes('video/mov') && !file.name.includes('video/wmv') && !file.name.includes('video/avi') && !file.name.includes('video/flv')) {
    //   this.fileError.emit('Only .mp4, .mov, .wmv, .avi video formats are supported.');
    //   this.uploadVideoForm.patchValue({
    //     file: null
    //   });
    // } else {
    //   this.formData.emit(file.size / 1000000 + ' Mb');
    // }
  }

  ngOnDestroy() {
    if (this.formEventSubscription) {
      this.formEventSubscription.unsubscribe();
    }
  }

}
