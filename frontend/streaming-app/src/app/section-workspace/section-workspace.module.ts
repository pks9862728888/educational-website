import { MaterialSectionWorkspaceModule } from './material-section-workspace';
import { InstituteApiService } from './../services/institute-api.service';
import { InAppDataTransferService } from './../services/in-app-data-transfer.service';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { sectionWorkspaceRoutingComponents, SectionWorkspaceRoutingModule } from './section-workspace-routing.module';



@NgModule({
  declarations: [
    sectionWorkspaceRoutingComponents
  ],
  imports: [
    CommonModule,
    SectionWorkspaceRoutingModule,
    MaterialSectionWorkspaceModule
  ],
  providers: [
    InAppDataTransferService,
    InstituteApiService
  ]
})
export class SectionWorkspaceModule { }
