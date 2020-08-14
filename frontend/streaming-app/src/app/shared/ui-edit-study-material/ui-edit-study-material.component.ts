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
      can_download: [this.filledFormText.data.can_download],
      target_date: [this.filledFormText.target_date]
    });
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
    data['view'] = this.filledFormText.view;
    if (data.target_date) {
      data['target_date'] = formatDate(data['target_date'])
    } else {
      data.pop('target_date');
    }
    this.formData.emit();
  }

  ngOnDestroy(): void {
    if (this.formEventSubscription) {
      this.formEventSubscription.unsubscribe();
    }
  }

}
