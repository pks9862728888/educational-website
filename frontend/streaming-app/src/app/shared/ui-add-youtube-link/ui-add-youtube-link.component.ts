import { Observable, Subscription } from 'rxjs';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, EventEmitter, Output, Input, OnDestroy } from '@angular/core';
import { Validators, FormBuilder, FormGroup } from '@angular/forms';
import { LECTURE_STUDY_MATERIAL_TYPES, SUBJECT_INTRODUCTION_CONTENT_TYPE_REVERSE } from '../../../constants';
import { formatDate } from '../../format-datepicker';

@Component({
  selector: 'app-ui-add-youtube-link',
  templateUrl: './ui-add-youtube-link.component.html',
  styleUrls: ['./ui-add-youtube-link.component.css']
})
export class UiAddYoutubeLinkComponent implements OnInit, OnDestroy {

  mq: MediaQueryList;
  uploadForm: FormGroup;
  showIndicator: boolean;
  @Input() showTargetDate: boolean;
  @Output() formFieldError = new EventEmitter<string>();
  @Output() formData = new EventEmitter<any>();
  @Input() formEvent: Observable<String>;
  private formEventSubscription: Subscription;

  constructor(
    private media: MediaMatcher,
    private formBuilder: FormBuilder
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.uploadForm = this.formBuilder.group({
      name: [null, [Validators.required, Validators.maxLength(20)]],
      link: [null, [Validators.required, Validators.maxLength(100)]],
      target_date: [null]
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
        }
      }
    );
  }

  upload() {
    this.uploadForm.patchValue({
      name: this.uploadForm.value.name.trim(),
      link: this.uploadForm.value.link.trim()
    })
    if (!this.uploadForm.value.name) {
      this.formFieldError.emit('Title can not be blank.');
    } else if (!this.uploadForm.value.link) {
      this.formFieldError.emit('Url can not be blank.');
    } else {
      let data = this.uploadForm.value;
      if (data['target_date']) {
        data['target_date'] = formatDate(data['target_date']);
      }
      data['content_type'] = LECTURE_STUDY_MATERIAL_TYPES['YOUTUBE_LINK'];
      this.formData.emit(data);
    }
  }

  ngOnDestroy() {
    if (this.formEventSubscription) {
      this.formEventSubscription.unsubscribe();
    }
  }
}
