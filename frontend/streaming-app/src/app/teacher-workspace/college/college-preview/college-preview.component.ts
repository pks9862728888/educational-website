import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, ParamMap } from '@angular/router';

@Component({
  selector: 'app-college-preview',
  templateUrl: './college-preview.component.html',
  styleUrls: ['./college-preview.component.css']
})
export class CollegePreviewComponent implements OnInit {

  // To store current institute details
  currentInstituteSlug: string;

  constructor( private route: ActivatedRoute ) { }

  ngOnInit(): void {
    this.route.paramMap
      .subscribe((params: ParamMap) => {
        this.currentInstituteSlug = params.get('name');
      });
    console.log(this.currentInstituteSlug);
  }

}
