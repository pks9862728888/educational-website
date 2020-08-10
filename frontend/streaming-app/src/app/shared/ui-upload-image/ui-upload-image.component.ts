import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, EventEmitter, Output, Input } from '@angular/core';
import { Validators, FormGroup, FormBuilder } from '@angular/forms';
import { formatDate } from '../../format-datepicker';

@Component({
  selector: 'app-ui-upload-image',
  templateUrl: './ui-upload-image.component.html',
  styleUrls: ['./ui-upload-image.component.css']
})
export class UiUploadImageComponent implements OnInit {

  mq: MediaQueryList;
  uploadImageForm: FormGroup;
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
    this.uploadImageForm = this.formBuilder.group({
      title: [null, [Validators.required, Validators.maxLength(30)]],
      file: [null, [Validators.required]],
      deadline: [null]
    });
  }

  processVideo() {
    const file: File = (<HTMLInputElement>document.getElementById('image-file')).files[0];
    console.log(file);
    console.log(formatDate(this.uploadImageForm.value.deadline));

    if (!file.type.includes('image/jpeg') && !file.name.includes('image/jpg') && !file.name.includes('image/png') && !file.name.includes('image/webp')) {
      this.fileError.emit('Only .jpeg, .jpg, .webp, and .png formats are supported.');
      this.uploadImageForm.patchValue({
        file: null
      });
    } else {
      this.formData.emit(file.size / 1000000 + ' Mb');
    }
  }
}
