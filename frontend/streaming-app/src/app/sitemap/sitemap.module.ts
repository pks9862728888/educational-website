import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SitemapRoutingModule, sitemapRoutingComponents } from './sitemap-routing.module';


@NgModule({
  declarations: [sitemapRoutingComponents],
  imports: [
    CommonModule,
    SitemapRoutingModule
  ]
})
export class SitemapModule { }
