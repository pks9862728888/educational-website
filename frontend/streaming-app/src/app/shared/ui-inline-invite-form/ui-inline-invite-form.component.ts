import { FormGroup, Validators, FormBuilder } from '@angular/forms';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Observable, Subscription } from 'rxjs';

@Component({
  selector: 'app-ui-inline-invite-form',
  templateUrl: './ui-inline-invite-form.component.html',
  styleUrls: ['./ui-inline-invite-form.component.css']
})
export class UiInlineInviteFormComponent implements OnInit {

  mq: MediaQueryList;
  inviteForm: FormGroup;
  @Input() createInviteIndicator: boolean;
  @Input() showInviteFormMb: boolean;
  @Input() inputPlaceholder: string;
  @Input() buttonText: string;
  @Input() hasPerm: boolean;
  @Output() showInviteFormMobile = new EventEmitter<void>();
  @Output() hideInviteFormMobile = new EventEmitter<void>();
  @Output() inviteeEmail = new EventEmitter<string>();
  @Input() formEvent: Observable<string>;
  private formEventSubscription: Subscription;

  constructor( private media: MediaMatcher,
               private formBuilder: FormBuilder ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.inviteForm = this.formBuilder.group({
      invitee: [null, [Validators.required, Validators.email]]
    });
    this.formEventSubscription = this.formEvent.subscribe(
      (status: string) => {
        if (status === 'enable') {
          this.inviteForm.enable();
        } else if (status === 'disable') {
          this.inviteForm.disable();
        } else if (status === 'reset') {
          this.inviteForm.reset();
          this.inviteForm.enable();
        }
      }
    );
  }

  invite() {
    this.inviteeEmail.emit(this.inviteForm.value.invitee);
  }

  showInviteFormMobile_() {
    this.showInviteFormMobile.emit();
  }

  hideInviteFormMobile_() {
    this.hideInviteFormMobile.emit();
  }

  ngOnDestroy() {
    if (this.formEventSubscription) {
      this.formEventSubscription.unsubscribe();
    }
  }
}
