import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HelpComponent } from './help.component';
import { AppRoutingModule } from '../app-routing.module';
import { HelpMaterialWorkspaceModule } from './material.help.module';



@NgModule({
  declarations: [HelpComponent],
  imports: [
    CommonModule,
    AppRoutingModule,
    HelpMaterialWorkspaceModule,
  ]
})
export class HelpModule { }
