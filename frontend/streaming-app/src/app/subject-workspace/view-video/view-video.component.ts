import { courseContent, currentSubjectSlug, hasSubjectPerm } from './../../../constants';
import { Component, OnInit, EventEmitter, Output, OnDestroy, } from '@angular/core';
import { StudyMaterialDetails } from '../../models/subject.model';
import { MediaMatcher } from '@angular/cdk/layout';
import { Subscription, Subject } from 'rxjs';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { UiService } from 'src/app/services/ui.service';


declare const videojs: any;


@Component({
  selector: 'app-view-video',
  templateUrl: './view-video.component.html',
  styleUrls: ['./view-video.component.css']
})
export class ViewVideoComponent implements OnInit, OnDestroy {

  content: StudyMaterialDetails;
  @Output() closeViewEvent = new EventEmitter();
  mq: MediaQueryList;
  player: any;


  constructor(
    private media: MediaMatcher
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.content = JSON.parse(sessionStorage.getItem(courseContent));
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

  back() {
      this.closeViewEvent.emit();
  }

  download() {
    const ext = this.content.data.file.split('.');
    saveAs(
      this.content.data.file, this.content.title.toLowerCase().replace(' ', '_') + '.' + ext[ext.length - 1]);
  }

  ngOnDestroy() {
    this.player.dispose();
  }

}
