import { Component, OnInit, EventEmitter, Input, Output } from '@angular/core';
import { Validators, FormGroup, FormBuilder } from '@angular/forms';
import { MediaMatcher } from '@angular/cdk/layout';

@Component({
  selector: 'app-ui-inline-create-form',
  templateUrl: './ui-inline-create-form.component.html',
  styleUrls: ['./ui-inline-create-form.component.css']
})
export class UiInlineCreateFormComponent implements OnInit {

  mq: MediaQueryList;
  newForm: FormGroup;
  @Input() createIndicator: boolean;
  @Input() showFormMb: boolean;
  @Input() inputPlaceholder: string;
  @Input() buttonText: string;
  @Input() hasPerm: boolean;
  @Input() maxLength: number;
  @Output() showFormMobile = new EventEmitter<void>();
  @Output() hideFormMobile = new EventEmitter<void>();
  @Output() createEvent = new EventEmitter<string>();

  constructor( private media: MediaMatcher,
               private formBuilder: FormBuilder ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.newForm = this.formBuilder.group({
      name: [null, [Validators.required, Validators.maxLength(this.maxLength)]]
    });
  }

  create() {
    this.newForm.patchValue({
      name: this.newForm.value.name.trim()
    });
    if (this.newForm.value.name.length > 0) {
      this.createEvent.emit(this.newForm.value.name);
    }
  }

  showFormMobile_() {
    this.showFormMobile.emit();
  }

  hideFormMobile_() {
    this.hideFormMobile.emit();
  }
}
