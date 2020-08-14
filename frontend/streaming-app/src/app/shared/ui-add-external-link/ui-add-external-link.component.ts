import { Observable, Subscription } from 'rxjs';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, EventEmitter, Output, Input, OnDestroy } from '@angular/core';
import { Validators, FormBuilder, FormGroup } from '@angular/forms';
import { STUDY_MATERIAL_CONTENT_TYPE_REVERSE } from '../../../constants';
import { formatDate } from '../../format-datepicker';

@Component({
  selector: 'app-ui-add-external-link',
  templateUrl: './ui-add-external-link.component.html',
  styleUrls: ['./ui-add-external-link.component.css']
})
export class UiAddExternalLinkComponent implements OnInit, OnDestroy {

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
      title: [null, [Validators.required, Validators.maxLength(20)]],
      url: [null, [Validators.required, Validators.maxLength(100)]],
      target_date: [null],
      description: [null],
      can_download: [true],
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
      title: this.uploadForm.value.title.trim(),
      url: this.uploadForm.value.url.trim(),
      description: this.uploadForm.value.description.trim()
    })
    if (!this.uploadForm.value.title) {
      this.formFieldError.emit('Title can not be blank.');
    } else if (!this.uploadForm.value.url) {
      this.formFieldError.emit('url can not be blank.');
    } else {
      let data = this.uploadForm.value;
      if (data['target_date']) {
        data['target_date'] = formatDate(data['target_date']);
      }
      data['content_type'] = STUDY_MATERIAL_CONTENT_TYPE_REVERSE['EXTERNAL_LINK'];
      this.formData.emit(data);
    }
  }

  ngOnDestroy() {
    if (this.formEventSubscription) {
      this.formEventSubscription.unsubscribe();
    }
  }
}
