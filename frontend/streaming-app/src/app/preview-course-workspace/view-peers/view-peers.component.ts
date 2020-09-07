import { InstituteApiService } from 'src/app/services/institute-api.service';
import { currentInstituteSlug, currentSubjectSlug } from './../../../constants';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { SubjectPeerDetails, SubjectPeersResponse } from '../../models/subject.model';

@Component({
  selector: 'app-view-peers',
  templateUrl: './view-peers.component.html',
  styleUrls: ['./view-peers.component.css']
})
export class ViewPeersComponent implements OnInit {

  mq: MediaQueryList;
  loadingIndicator: boolean;
  reloadIndicator: boolean;
  errorText: string;
  currentInstituteSlug: string;
  currentSubjectSlug: string;

  viewOrder: Array<string> = [];
  students: SubjectPeerDetails[] = [];
  instructors: SubjectPeerDetails[] = [];

  constructor(
    private media: MediaMatcher,
    private instituteApiService: InstituteApiService
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.currentSubjectSlug = sessionStorage.getItem(currentSubjectSlug);
  }

  ngOnInit(): void {
    this.getCoursePeers();
  }

  getCoursePeers() {
   this.loadingIndicator = true;
   this.reloadIndicator = false;
   this.errorText = null;
   this.instituteApiService.getCoursePeers(
     this.currentInstituteSlug,
     this.currentSubjectSlug
   ).subscribe(
     (result: SubjectPeersResponse) => {
       this.loadingIndicator = false;
       this.viewOrder = result.view_order;
       this.students = result.students;
       this.instructors = result.instructors;
       console.log(result);
     },
     errors => {
       this.loadingIndicator = false;
       if (errors.error) {
         if (errors.error.error) {
           this.errorText = errors.error.error;
         } else {
           this.reloadIndicator = true;
         }
       } else {
         this.reloadIndicator = true;
       }
     }
   )

  }

  getMembersList(index: number) {
    if (index === 0) {
      return this.instructors;
    } else {
      return this.students;
    }
  }

  getMembersCount(index: number) {
    if (index === 0) {
      return this.instructors.length;
    } else {
      return this.students.length;
    }
  }

}
