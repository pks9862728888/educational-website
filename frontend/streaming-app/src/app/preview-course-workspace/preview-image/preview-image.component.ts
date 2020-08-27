import { MediaMatcher } from '@angular/cdk/layout';
import { StudyMaterialPreviewDetails } from './../../models/subject.model';
import { Component, OnInit } from '@angular/core';
import { previewActionContent } from '../../../constants';
import { saveAs } from 'file-saver';

@Component({
  selector: 'app-preview-image',
  templateUrl: './preview-image.component.html',
  styleUrls: ['./preview-image.component.css']
})
export class PreviewImageComponent implements OnInit {

  mq: MediaQueryList;
  content: StudyMaterialPreviewDetails;
  filename: string;

  constructor(
    private media: MediaMatcher
  ) {
    this.content = JSON.parse(sessionStorage.getItem(previewActionContent));
    const ext = this.content.data.file.split('.');
    this.filename = this.content.title.toLowerCase().replace(' ', '_') + '.' + ext[ext.length - 1];
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
  }

  download() {
    const ext = this.content.data.file.split('.');
    saveAs(
      this.content.data.file, this.content.title.toLowerCase().replace(' ', '_') + '.' + ext[ext.length - 1]);
  }

}
