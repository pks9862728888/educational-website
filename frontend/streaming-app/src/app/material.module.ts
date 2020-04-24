import { NgModule } from '@angular/core';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { MatCheckboxModule } from '@angular/material/checkbox';

@NgModule({
    imports: [MatInputModule,
              MatFormFieldModule,
              MatButtonModule,
              MatCheckboxModule],
    exports: [MatInputModule,
              MatFormFieldModule,
              MatButtonModule,
              MatCheckboxModule]
})
export class MaterialModule {}
