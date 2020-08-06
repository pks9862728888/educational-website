import { SharedModule } from './../shared/shared.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { InstituteApiService } from './../services/institute-api.service';
import { InAppDataTransferService } from './../services/in-app-data-transfer.service';
import { classWorkspaceRoutingComponents, ClassWorkspaceRoutingModule } from './class-workspace-routing.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MaterialClassWorkspaceModule } from './material.class.workspace';
import { ClassSectionComponent } from './class-section/class-section.component';


@NgModule({
  declarations: [
    classWorkspaceRoutingComponents,
    ClassSectionComponent,
  ],
  imports: [
    CommonModule,
    ClassWorkspaceRoutingModule,
    MaterialClassWorkspaceModule,
    FormsModule,
    ReactiveFormsModule,
    SharedModule
  ],
  providers: [
    InAppDataTransferService,
    InstituteApiService
  ]
})
export class ClassWorkspaceModule { }
