import { Component, OnInit, EventEmitter, Input, Output, OnChanges, SimpleChange, SimpleChanges, OnDestroy } from '@angular/core';
import { Validators, FormGroup, FormBuilder } from '@angular/forms';
import { MediaMatcher } from '@angular/cdk/layout';
import { Observable, Subscription } from 'rxjs';

@Component({
  selector: 'app-ui-inline-create-form',
  templateUrl: './ui-inline-create-form.component.html',
  styleUrls: ['./ui-inline-create-form.component.css']
})
export class UiInlineCreateFormComponent implements OnInit, OnDestroy {

  mq: MediaQueryList;
  createForm: FormGroup;
  @Input() createIndicator: boolean;
  @Input() showFormMb: boolean;
  @Input() inputPlaceholder: string;
  @Input() buttonText: string;
  @Input() maxLength: number;
  @Output() showFormMobile = new EventEmitter<void>();
  @Output() hideFormMobile = new EventEmitter<void>();
  @Output() createEvent = new EventEmitter<string>();
  @Input() formEvent: Observable<string>;
  private formEventSubscription: Subscription;

  constructor( private media: MediaMatcher,
               private formBuilder: FormBuilder ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.createForm = this.formBuilder.group({
      name: [null, [Validators.required, Validators.maxLength(this.maxLength)]]
    });

    this.formEventSubscription = this.formEvent.subscribe(
      (status: string) => {
        if (status === 'disable') {
          this.createForm.disable();
        } else if (status === 'enable') {
          this.createForm.enable();
        } else if (status === 'reset') {
          this.createForm.reset();
          this.createForm.enable();
        }
      }
    );
  }

  create() {
    this.createForm.patchValue({
      name: this.createForm.value.name.trim()
    });
    if (this.createForm.value.name.length > 0) {
      this.createEvent.emit(this.createForm.value.name);
    }
  }

  showFormMobile_() {
    this.showFormMobile.emit();
  }

  hideFormMobile_() {
    this.hideFormMobile.emit();
  }

  ngOnDestroy() {
    if (this.formEventSubscription) {
      this.formEventSubscription.unsubscribe();
    }
  }
}
