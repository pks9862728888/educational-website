import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { authRoutingComponents, AuthRoutingModule } from './auth-routing.module';
import { AuthMaterialModule } from './material.auth.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FlexLayoutModule } from '@angular/flex-layout';
import { AuthService } from '../auth.service';


@NgModule({
  declarations: [authRoutingComponents],
  imports: [
    CommonModule,
    AuthMaterialModule,
    AuthRoutingModule,
    FlexLayoutModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  providers: [AuthService]
})
export class AuthModule { }
