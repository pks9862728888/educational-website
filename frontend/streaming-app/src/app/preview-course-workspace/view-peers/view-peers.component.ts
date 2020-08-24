import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-view-peers',
  templateUrl: './view-peers.component.html',
  styleUrls: ['./view-peers.component.css']
})
export class ViewPeersComponent implements OnInit {

  mq: MediaQueryList;

  constructor(
    private media: MediaMatcher
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
  }

}
