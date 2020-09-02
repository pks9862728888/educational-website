import { SharedModule } from './../shared/shared.module';
import { UiService } from './../services/ui.service';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { TeacherMaterialWorkspaceModule } from './material.teacher.workspace.module';
import { TeacherWorkspaceRoutingModule, teacherWorkspaceRoutingComponents } from './teacher-workspace-routing.module';
import { CreateInstituteComponent } from './teacher-institute/create-institute/create-institute.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { ApiService } from '../services/api.service';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule, DateAdapter, MAT_DATE_FORMATS } from '@angular/material/core';
import { AppDateAdapter, APP_DATE_FORMATS } from '../format-datepicker';
import { InAppDataTransferService } from '../services/in-app-data-transfer.service';


@NgModule({
  declarations: [
    CreateInstituteComponent,
    teacherWorkspaceRoutingComponents
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    FlexLayoutModule,
    TeacherMaterialWorkspaceModule,
    TeacherWorkspaceRoutingModule,
    MatDatepickerModule,
    MatNativeDateModule,
    SharedModule
  ],
  providers: [
    ApiService,
    UiService,
    InAppDataTransferService,
    {provide: DateAdapter, useClass: AppDateAdapter},
    {provide: MAT_DATE_FORMATS, useValue: APP_DATE_FORMATS}
  ],
  entryComponents: []
})
export class TeacherWorkspaceModule { }
