import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-ui-success-text',
  templateUrl: './ui-success-text.component.html',
  styleUrls: ['./ui-success-text.component.css']
})
export class UiSuccessTextComponent {

  @Input() successText: string;
  @Output() closeSuccessTextEvent = new EventEmitter<void>();

  constructor() { }

  hideSuccessText() {
    this.closeSuccessTextEvent.emit();
  }
}
