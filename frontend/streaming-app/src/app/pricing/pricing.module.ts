import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PricingComponent } from './pricing.component';
import { AppRoutingModule } from '../app-routing.module';
import { PricingMaterialWorkspaceModule } from './material.pricing.module';



@NgModule({
  declarations: [PricingComponent],
  imports: [
    CommonModule,
    AppRoutingModule,
    PricingMaterialWorkspaceModule,
  ]
})
export class PricingModule { }
