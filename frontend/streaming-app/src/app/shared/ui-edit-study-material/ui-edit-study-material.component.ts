import { STUDY_MATERIAL_CONTENT_TYPE_REVERSE } from './../../../constants';
import { MediaMatcher } from '@angular/cdk/layout';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Subscription, Observable } from 'rxjs';
import { Component, OnInit, Input, OnDestroy, Output, EventEmitter } from '@angular/core';
import { StudyMaterialDetails } from '../../models/subject.model';
import { formatDate } from '../../format-datepicker';


@Component({
  selector: 'app-ui-edit-study-material',
  templateUrl: './ui-edit-study-material.component.html',
  styleUrls: ['./ui-edit-study-material.component.css']
})
export class UiEditStudyMaterialComponent implements OnInit, OnDestroy {

  @Input() showTargetDate: boolean;
  @Input() filledFormText: StudyMaterialDetails;
  @Input() formEvent: Observable<string>;
  @Output() formData = new EventEmitter();
  formEventSubscription: Subscription;
  editForm: FormGroup;
  showIndicator: boolean;
  mq: MediaQueryList;

  constructor(
    private formBuilder: FormBuilder,
    private media: MediaMatcher
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.editForm = this.formBuilder.group({
      title: [this.filledFormText.title, [Validators.required]],
      description: [this.filledFormText.description],
      target_date: [this.filledFormText.target_date],
      data: this.formBuilder.group({
        can_download: [],
        url: [],
      })
    });
    if (this.notExternalLinkView()) {
      this.editForm.patchValue({
        data: {
          can_download: this.filledFormText.data.can_download
        }
      })
    } else {
      this.editForm.patchValue({
        data: {
          url: this.filledFormText.data.url
        }
      })
    }
    this.formEventSubscription = this.formEvent.subscribe(
      (data: string) => {
        if (data === 'ENABLE') {
          this.showIndicator = false;
          this.editForm.enable();
        } else if (data === 'DISABLE') {
          this.showIndicator = true;
          this.editForm.disable();
        } else if (data === 'RESET') {
          this.showIndicator = false;
          this.editForm.reset();
          this.editForm.enable();
        }
      }
    );
  }

  submit() {
    const data = this.editForm.value;
    data['content_type'] = this.filledFormText.content_type
    if (data.target_date) {
      data['target_date'] = formatDate(data['target_date'])
    }
    if (this.notExternalLinkView()) {
      delete data['data']['url'];
    } else {
      delete data['data']['can_download'];
    }
    this.formData.emit(data);
  }

  notExternalLinkView() {
    if (this.filledFormText.content_type !== STUDY_MATERIAL_CONTENT_TYPE_REVERSE['EXTERNAL_LINK']) {
      return true;
    } else {
      return false;
    }
  }

  ngOnDestroy(): void {
    if (this.formEventSubscription) {
      this.formEventSubscription.unsubscribe();
    }
  }

}
