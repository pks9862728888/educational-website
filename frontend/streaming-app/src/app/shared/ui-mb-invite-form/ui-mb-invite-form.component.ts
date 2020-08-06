import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Component, OnInit, Input, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-ui-mb-invite-form',
  templateUrl: './ui-mb-invite-form.component.html',
  styleUrls: ['./ui-mb-invite-form.component.css']
})
export class UiMbInviteFormComponent implements OnInit {

  newInviteForm: FormGroup;
  @Input() createInviteIndicator: boolean;
  @Input() inputPlaceholder: string;
  @Input() buttonText: string;
  @Input() progressSpinnerText: string;
  @Output() inviteeEmail = new EventEmitter<string>();

  constructor( private formBuilder: FormBuilder ) { }

  ngOnInit(): void {
    this.newInviteForm = this.formBuilder.group({
      invitee: [null, [Validators.required, Validators.email]]
    });
  }

  invite() {
    this.inviteeEmail.emit(this.newInviteForm.value.invitee);
  }

}
