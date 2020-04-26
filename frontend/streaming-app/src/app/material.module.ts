import { NgModule } from '@angular/core';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';

@NgModule({
    imports: [MatInputModule,
              MatFormFieldModule,
              MatButtonModule,
              MatCheckboxModule,
              MatIconModule,
              MatDividerModule],
    exports: [MatInputModule,
              MatFormFieldModule,
              MatButtonModule,
              MatCheckboxModule,
              MatIconModule,
              MatDividerModule]
})
export class MaterialModule {}
