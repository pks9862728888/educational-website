import { Component, OnInit, EventEmitter, Input, Output, OnDestroy } from '@angular/core';
import { FormGroup, Validators, FormBuilder } from '@angular/forms';
import { Observable, Subscription } from 'rxjs';

@Component({
  selector: 'app-ui-mb-create-form',
  templateUrl: './ui-mb-create-form.component.html',
  styleUrls: ['./ui-mb-create-form.component.css']
})
export class UiMbCreateFormComponent implements OnInit, OnDestroy {

  createForm: FormGroup;
  @Input() patchFormNameData: string;
  @Input() maxLength: number;
  @Input() createIndicator: boolean;
  @Input() inputPlaceholder: string;
  @Input() buttonText: string;
  @Input() progressSpinnerText: string;
  @Output() createEvent = new EventEmitter<string>();
  @Input() formEvent: Observable<string>;
  private formEventSubscription: Subscription;

  constructor( private formBuilder: FormBuilder ) { }

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
    if (this.patchFormNameData) {
      this.createForm.patchValue({
        name: this.patchFormNameData
      });
    }
  }

  create() {
    this.createForm.patchValue({
      name: this.createForm.value.name.trim()
    })
    if (this.createForm.value.name.length > 0) {
      this.createEvent.emit(this.createForm.value.name);
    }
  }

  ngOnDestroy() {
    if (this.formEventSubscription) {
      this.formEventSubscription.unsubscribe();
    }
  }
}
