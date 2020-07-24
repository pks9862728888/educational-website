import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PricingRoutingModule, pricingRoutingComponents } from './pricing-routing.module';
import { PricingMaterialWorkspaceModule } from './material.pricing.module';


@NgModule({
  declarations: [
    pricingRoutingComponents
  ],
  imports: [
    CommonModule,
    PricingRoutingModule,
    PricingMaterialWorkspaceModule,
  ]
})
export class PricingModule { }
