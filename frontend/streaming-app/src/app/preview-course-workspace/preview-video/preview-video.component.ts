import { MediaMatcher } from '@angular/cdk/layout';
import { previewActionContent } from './../../../constants';
import { StudyMaterialPreviewDetails } from './../../models/subject.model';
import { Component, OnInit, Output, EventEmitter } from '@angular/core';

declare const videojs: any;

@Component({
  selector: 'app-preview-video',
  templateUrl: './preview-video.component.html',
  styleUrls: ['./preview-video.component.css']
})
export class PreviewVideoComponent implements OnInit {

  mq: MediaQueryList;
  player: any;
  content: StudyMaterialPreviewDetails;

  constructor(
    private media: MediaMatcher
  ) {
    this.content = JSON.parse(sessionStorage.getItem(previewActionContent));
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.player = videojs(document.getElementById('video-player'));
    this.player.src({
      src: this.content.data.stream_file,
      type: 'application/x-mpegURL'
    });
    this.player.hlsQualitySelector({
      displayCurrentQuality: true,
    });
  }
}
