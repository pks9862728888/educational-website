import { InstituteApiService } from './../services/institute-api.service';
import { InAppDataTransferService } from './../services/in-app-data-transfer.service';
import { classWorkspaceRoutingComponents, ClassWorkspaceRoutingModule } from './class-workspace-routing.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MaterialClassWorkspaceModule } from './material.class.workspace';


@NgModule({
  declarations: [
    classWorkspaceRoutingComponents,
  ],
  imports: [
    CommonModule,
    ClassWorkspaceRoutingModule,
    MaterialClassWorkspaceModule
  ],
  providers: [
    InAppDataTransferService,
    InstituteApiService
  ]
})
export class ClassWorkspaceModule { }
