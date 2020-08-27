import { MediaMatcher } from '@angular/cdk/layout';
import { StudyMaterialPreviewDetails } from './../../models/subject.model';
import { Component, OnInit } from '@angular/core';
import { previewActionContent } from '../../../constants';

@Component({
  selector: 'app-preview-pdf',
  templateUrl: './preview-pdf.component.html',
  styleUrls: ['./preview-pdf.component.css']
})
export class PreviewPdfComponent implements OnInit {

  mq: MediaQueryList;
  content: StudyMaterialPreviewDetails;
  filename: string;

  constructor(
    private media: MediaMatcher
  ) {
    this.content = JSON.parse(sessionStorage.getItem(previewActionContent));
    const ext = this.content.data.file.split('.');
    this.filename = this.content.title.toLowerCase().replace(' ', '_') + '.' + ext[ext.length - 1];
  }

  ngOnInit(): void {}

}
