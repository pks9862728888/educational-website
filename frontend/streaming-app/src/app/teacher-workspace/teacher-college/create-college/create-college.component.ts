import { Component, OnInit } from '@angular/core';

interface StateInterface {
  value: string;
  viewValue: String;
}

@Component({
  selector: 'app-create-college',
  templateUrl: './create-college.component.html',
  styleUrls: ['./create-college.component.css']
})
export class CreateCollegeComponent implements OnInit {

  state: StateInterface[] = [
    {value: 'AN', viewValue: 'ANDAMAN AND NICOBAR ISLANDS'},
    {value: 'AP', viewValue: 'ANDHRA PRADESH'},
  ];

  constructor() { }

  ngOnInit(): void {
  }

}
