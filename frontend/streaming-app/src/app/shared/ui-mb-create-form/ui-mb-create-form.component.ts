import { Component, OnInit, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup, Validators, FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-ui-mb-create-form',
  templateUrl: './ui-mb-create-form.component.html',
  styleUrls: ['./ui-mb-create-form.component.css']
})
export class UiMbCreateFormComponent implements OnInit {

  createForm: FormGroup;
  @Input() maxLength: number;
  @Input() createIndicator: boolean;
  @Input() inputPlaceholder: string;
  @Input() buttonText: string;
  @Input() progressSpinnerText: string;
  @Output() createEvent = new EventEmitter<string>();

  constructor( private formBuilder: FormBuilder ) { }

  ngOnInit(): void {
    this.createForm = this.formBuilder.group({
      name: [null, [Validators.required, Validators.maxLength(this.maxLength)]]
    });
  }

  create() {
    this.createForm.patchValue({
      name: this.createForm.value.name.trim()
    })
    if (this.createForm.value.name.length > 0) {
      this.createEvent.emit(this.createForm.value.name);
    }
  }
}
