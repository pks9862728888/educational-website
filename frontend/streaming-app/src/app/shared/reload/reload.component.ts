import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-reload',
  templateUrl: './reload.component.html',
  styleUrls: ['./reload.component.css']
})
export class ReloadComponent implements OnInit {

  mobileQuery: MediaQueryList;

  @Input() errorText: string;
  @Output() retryEvent = new EventEmitter<void>();

  constructor( private media: MediaMatcher) {
    this.mobileQuery = this.media.matchMedia('(max-width: 540px)');
  }

  ngOnInit(): void {}

  retry() {
    this.retryEvent.emit();
  }
}
