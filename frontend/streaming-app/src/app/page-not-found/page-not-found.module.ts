import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PageNotFoundRoutingModule, pageNotFoundRoutingComponents } from './page-not-found-routing.module';


@NgModule({
  declarations: [pageNotFoundRoutingComponents],
  imports: [
    CommonModule,
    PageNotFoundRoutingModule
  ]
})
export class PageNotFoundModule { }
