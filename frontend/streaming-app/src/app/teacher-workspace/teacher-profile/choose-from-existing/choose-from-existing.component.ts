import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/api.service';
import { MediaMatcher } from '@angular/cdk/layout';

@Component({
  selector: 'app-choose-from-existing',
  templateUrl: './choose-from-existing.component.html',
  styleUrls: ['./choose-from-existing.component.css']
})
export class ChooseFromExistingComponent implements OnInit {

  // For detecting whether device is mobile
  mobileQuery: MediaQueryList;

  constructor(private media: MediaMatcher,
              private apiService: ApiService) {
      this.mobileQuery = media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
  }

}
