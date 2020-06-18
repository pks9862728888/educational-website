import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FeaturesComponent } from './features.component';
import { FeaturesMaterialWorkspaceModule } from './material.features.module';
import { AppRoutingModule } from '../app-routing.module';



@NgModule({
  declarations: [FeaturesComponent],
  imports: [
    CommonModule,
    AppRoutingModule,
    FeaturesMaterialWorkspaceModule,
  ]
})
export class FeaturesModule { }
