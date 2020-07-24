import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FeaturesMaterialWorkspaceModule } from './material.features.module';
import { FeaturesRoutingModule, featuresRouteComponents } from './features-routing.module';


@NgModule({
  declarations: [featuresRouteComponents],
  imports: [
    CommonModule,
    FeaturesMaterialWorkspaceModule,
    FeaturesRoutingModule
  ]
})
export class FeaturesModule { }
