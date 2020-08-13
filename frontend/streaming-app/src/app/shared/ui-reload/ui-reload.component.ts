import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-ui-reload',
  templateUrl: './ui-reload.component.html',
  styleUrls: ['./ui-reload.component.css']
})
export class UiReloadComponent implements OnInit {

  mq: MediaQueryList;

  @Input() errorText: string;
  @Output() retryEvent = new EventEmitter<void>();

  constructor( private media: MediaMatcher) {
    this.mq = this.media.matchMedia('(max-width: 540px)');
  }

  ngOnInit(): void {}

  retry() {
    this.retryEvent.emit();
  }
}
