import { FormGroup, Validators, FormBuilder } from '@angular/forms';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-ui-inline-invite-form',
  templateUrl: './ui-inline-invite-form.component.html',
  styleUrls: ['./ui-inline-invite-form.component.css']
})
export class UiInlineInviteFormComponent implements OnInit {

  mq: MediaQueryList;
  newInviteForm: FormGroup;
  @Input() createInviteIndicator: boolean;
  @Input() showInviteFormMb: boolean;
  @Input() inputPlaceholder: string;
  @Input() buttonText: string;
  @Input() hasPerm: boolean;
  @Output() showInviteFormMobile = new EventEmitter<void>();
  @Output() hideInviteFormMobile = new EventEmitter<void>();
  @Output() inviteeEmail = new EventEmitter<string>();

  constructor( private media: MediaMatcher,
               private formBuilder: FormBuilder ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.newInviteForm = this.formBuilder.group({
      invitee: [null, [Validators.required, Validators.email]]
    });
  }

  invite() {
    this.inviteeEmail.emit(this.newInviteForm.value.invitee);
  }

  showInviteFormMobile_() {
    this.showInviteFormMobile.emit();
  }

  hideInviteFormMobile_() {
    this.hideInviteFormMobile.emit();
  }

}
