import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HelpRoutingModule, helpRoutingComponents } from './help-routing.module';
import { HelpMaterialWorkspaceModule } from './material.help.module';



@NgModule({
  declarations: [helpRoutingComponents],
  imports: [
    CommonModule,
    HelpRoutingModule,
    HelpMaterialWorkspaceModule,
  ]
})
export class HelpModule { }
