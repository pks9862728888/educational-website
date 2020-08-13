import { MediaMatcher } from '@angular/cdk/layout';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Component, OnInit, EventEmitter, Output, Input } from '@angular/core';
import { formatDate } from '../../format-datepicker';


@Component({
  selector: 'app-ui-upload-video',
  templateUrl: './ui-upload-video.component.html',
  styleUrls: ['./ui-upload-video.component.css']
})
export class UiUploadVideoComponent implements OnInit {

  mq: MediaQueryList;
  uploadVideoForm: FormGroup;
  @Input() showDeadline: boolean;
  @Output() formData = new EventEmitter<any>();
  @Output() fileError = new EventEmitter<string>();

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
      deadline: [null]
    });
  }

  processVideo() {
    const file: File = (<HTMLInputElement>document.getElementById('video-file')).files[0];
    console.log(file);
    console.log(formatDate(this.uploadVideoForm.value.deadline));

    // if (!file.type.includes('video/mp4') && !file.name.includes('video/mov') && !file.name.includes('video/wmv') && !file.name.includes('video/avi') && !file.name.includes('video/flv')) {
    //   this.fileError.emit('Only .mp4, .mov, .wmv, .avi video formats are supported.');
    //   this.uploadVideoForm.patchValue({
    //     file: null
    //   });
    // } else {
    //   this.formData.emit(file.size / 1000000 + ' Mb');
    // }
  }

}
