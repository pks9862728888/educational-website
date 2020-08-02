import { SharedModule } from './../shared/shared.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule, DateAdapter, MAT_DATE_FORMATS } from '@angular/material/core';
import { APP_DATE_FORMATS, AppDateAdapter } from '../format-datepicker';
import { InAppDataTransferService } from '../services/in-app-data-transfer.service';
import { CollegeMaterialWorkspaceModule } from './material.college.workspace.module';
import { CollegeWorkspaceRoutingModule, collegeWorkspaceRoutingComponents } from './college-workspace-routing.module';
import { LicenseModule } from '../license/license.module';
import { ApiService } from '../services/api.service';


@NgModule({
  declarations: [collegeWorkspaceRoutingComponents],
  imports: [
    CommonModule,
    CollegeWorkspaceRoutingModule,
    CollegeMaterialWorkspaceModule,
    LicenseModule,
    FormsModule,
    ReactiveFormsModule,
    FlexLayoutModule,
    MatDatepickerModule,
    MatNativeDateModule,
    SharedModule
  ],
  providers: [
    ApiService,
    InAppDataTransferService,
    {provide: DateAdapter, useClass: AppDateAdapter},
    {provide: MAT_DATE_FORMATS, useValue: APP_DATE_FORMATS}
  ]
})
export class CollegeWorkspaceModule { }
