import { SUBJECT_INTRODUCTION_CONTENT_TYPE_REVERSE } from './../../../constants';
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

  @Input() showCancelButton: boolean;
  @Input() showTargetDate: boolean;
  @Input() filledFormText: any;
  @Input() formEvent: Observable<string>;
  @Output() formData = new EventEmitter();
  @Output() closeEvent = new EventEmitter<any>();
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
      name: [this.filledFormText.name, [Validators.required]],
      target_date: [this.filledFormText.target_date],
      can_download: [],
      link: []
    });
    if (this.notExternalLinkView()) {
      this.editForm.patchValue({
        can_download: this.filledFormText.data.can_download
      });
    } else {
      this.editForm.patchValue({
          link: this.filledFormText.data.link
      });
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
    if (!data.can_download) {
      data.can_download = false;
    }
    data.content_type = this.filledFormText.content_type;
    if (data.target_date) {
      data.target_date = formatDate(data.target_date);
    } else {
      delete data.target_date;
    }
    if (this.notExternalLinkView()) {
      delete data.link;
    } else {
      delete data.can_download;
    }
    data.id = this.filledFormText.id;
    this.formData.emit(data);
  }

  notExternalLinkView() {
    if (this.filledFormText.content_type !== SUBJECT_INTRODUCTION_CONTENT_TYPE_REVERSE.LINK) {
      return true;
    } else {
      return false;
    }
  }

  closeClicked() {
    this.closeEvent.emit(this.filledFormText);
  }

  ngOnDestroy(): void {
    if (this.formEventSubscription) {
      this.formEventSubscription.unsubscribe();
    }
  }
}
