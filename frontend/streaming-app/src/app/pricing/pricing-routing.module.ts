import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { PricingComponent } from './pricing.component';

const routes: Routes = [
  {
    path: '',
    component: PricingComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PricingRoutingModule {}

export const pricingRoutingComponents = [
  PricingComponent
];
