import { Component, OnInit } from '@angular/core';
import { InAppDataTransferService } from 'src/app/in-app-data-transfer.service';

@Component({
  selector: 'app-teacher-chatroom',
  templateUrl: './teacher-chatroom.component.html',
  styleUrls: ['./teacher-chatroom.component.css']
})
export class TeacherChatroomComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
    localStorage.setItem('activeRoute', 'CHATROOMS');
  }

}
