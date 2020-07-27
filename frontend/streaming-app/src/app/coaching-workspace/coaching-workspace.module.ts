import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule, DateAdapter, MAT_DATE_FORMATS } from '@angular/material/core';
import { ApiService } from '../services/api.service';
import { APP_DATE_FORMATS, AppDateAdapter } from '../format-datepicker';
import { InAppDataTransferService } from '../in-app-data-transfer.service';

import { CoachingMaterialWorkspaceModule } from './material.coaching.workspace.module';
import { coachingWorkspaceRoutingComponents, CoachingWorkspaceRoutingModule } from './coaching-workspace-routing.module';
import { LicenseModule } from '../license/license.module';


@NgModule({
  declarations: [coachingWorkspaceRoutingComponents],
  imports: [
    CommonModule,
    CoachingWorkspaceRoutingModule,
    LicenseModule,
    FormsModule,
    ReactiveFormsModule,
    FlexLayoutModule,
    CoachingMaterialWorkspaceModule,
    MatDatepickerModule,
    MatNativeDateModule
  ],
  providers: [
    ApiService,
    InAppDataTransferService,
    {provide: DateAdapter, useClass: AppDateAdapter},
    {provide: MAT_DATE_FORMATS, useValue: APP_DATE_FORMATS}
  ]
})
export class CoachingWorkspaceModule { }
