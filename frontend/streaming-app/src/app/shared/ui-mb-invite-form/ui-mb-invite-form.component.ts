import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Component, OnInit, Input, EventEmitter, Output, OnDestroy } from '@angular/core';
import { Observable, Subscription } from 'rxjs';

@Component({
  selector: 'app-ui-mb-invite-form',
  templateUrl: './ui-mb-invite-form.component.html',
  styleUrls: ['./ui-mb-invite-form.component.css']
})
export class UiMbInviteFormComponent implements OnInit, OnDestroy {

  inviteForm: FormGroup;
  @Input() createInviteIndicator: boolean;
  @Input() inputPlaceholder: string;
  @Input() buttonText: string;
  @Input() progressSpinnerText: string;
  @Output() inviteeEmail = new EventEmitter<string>();
  @Input() formEvent: Observable<string>;
  private formEventSubscription: Subscription;

  constructor( private formBuilder: FormBuilder ) { }

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

  ngOnDestroy() {
    if (this.formEventSubscription) {
      this.formEventSubscription.unsubscribe();
    }
  }
}
