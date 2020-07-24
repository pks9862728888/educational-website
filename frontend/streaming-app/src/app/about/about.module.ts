import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AboutComponent } from './about.component';
import { AboutRoutingModule, aboutRoutingComponents } from './about-routing.module';
import { AboutMaterialWorkspaceModule } from './material.about.module';



@NgModule({
  declarations: [aboutRoutingComponents],
  imports: [
    CommonModule,
    AboutRoutingModule,
    AboutMaterialWorkspaceModule,
  ]
})
export class AboutModule { }
