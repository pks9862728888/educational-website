import { InstituteApiService } from './../services/institute-api.service';
import { InAppDataTransferService } from './../services/in-app-data-transfer.service';
import { SharedModule } from './../shared/shared.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { subjectWorkspaceRoutingComponents, SubjectWorkspaceRoutingModule } from './subject-workspace-routing.module';
import { MaterialSubjectWorkspaceModule } from './material-subject-workspace';



@NgModule({
  declarations: [
    subjectWorkspaceRoutingComponents,
  ],
  imports: [
    CommonModule,
    SubjectWorkspaceRoutingModule,
    MaterialSubjectWorkspaceModule,
    SharedModule
  ],
  providers: [
    InstituteApiService,
    InAppDataTransferService
  ]
})
export class SubjectWorkspaceModule { }
