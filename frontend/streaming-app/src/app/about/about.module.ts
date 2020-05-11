import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AboutComponent } from './about.component';
import { AppRoutingModule } from '../app-routing.module';
import { AboutMaterialWorkspaceModule } from './material.about.module';



@NgModule({
  declarations: [AboutComponent],
  imports: [
    CommonModule,
    AppRoutingModule,
    AboutMaterialWorkspaceModule,
  ]
})
export class AboutModule { }
