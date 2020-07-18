import { Component, OnInit } from '@angular/core';
import { InAppDataTransferService } from 'src/app/in-app-data-transfer.service';

@Component({
  selector: 'app-classes',
  templateUrl: './classes.component.html',
  styleUrls: ['./classes.component.css']
})
export class ClassesComponent implements OnInit {

  constructor( private inAppDataTransferService: InAppDataTransferService ) { }

  ngOnInit(): void {
    localStorage.setItem('activeRoute', 'INSTITUTE_CLASSES');
    this.inAppDataTransferService.showInstituteSidenavView(true);
  }

}
